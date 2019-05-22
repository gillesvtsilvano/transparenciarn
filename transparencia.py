import requests
from orgao import OrgaoRN
from servidor import ServidorRN
from bs4 import BeautifulSoup

class TransparenciaRN:

    # Definindo a url alvo
    #url = 'http://servicos.searh.rn.gov.br/searh/Remuneracao/RemuneracaoPorId/16612356?MesAno=04%2F2019'
    url_base = 'http://servicos.searh.rn.gov.br/searh/Remuneracao'
    url_orgs = 'http://servicos.searh.rn.gov.br/searh/Remuneracao/Remuneracao'
    url_org_data = 'http://servicos.searh.rn.gov.br/searh/Remuneracao/RemuneracaoPorId'
    url_org_pag = 'http://servicos.searh.rn.gov.br/searh/Remuneracao/Paginados?pagina='

    month = ''
    year = ''
    search_for = '0' # Organization
    search_name = '' # nothing yet
    orgs = {}
    token = ''
    mime_type = 'application/x-www-form-urlencoded'
    token = ''

    months = {
        'Janeiro': '01',
        'Fevereiro': '02',
        'Março': '03',
        'Abril': '04',
        'Maio': '05',
        'Junho': '06',
        'Julho': '07',
        'Agosto': '08',
        'Setembro': '09',
        'Outubro': '10',
        'Novembro': '11',
        'Dezembro': '12'
    }

    def __init__(self, month, year, orgs=None):
        self.month = month
        self.year = year
        print('Creating HTTP Session...', end='')
        self.session = requests.session()
        print('Ok!'
              if self.session else 'Error creating HTTP Session. Exiting...' and exit(1))

        print('Acquiring token access...', end='')
        self.get_token()
        print(self.token[:5] + '...' + self.token[-5:] + '!'
              if self.token != '' else 'Could not acquire access token! Exiting...' and exit(1))
        print('Finding organizations...', end='')
        self.get_orgs()
        print('Found {}!'.format(len(self.orgs)))

        if not orgs:
            for _,v in self.orgs.items():
                print(v.name + '...', end=''),
                self.get_org_employees(v)
                print('Found {}!'.format())
        else:
            for org_name in orgs:
                print(org_name + '...', end='')
                org = self.get_org(org_name)
                self.get_org_employees(org)




    def get_token(self):
        response = self.session.get(self.url_base)
        
        #self.token = response.text.split('__RequestVerificationToken')[1].split('value=')[1].split(' ')[0][1:-1]
        for tag in BeautifulSoup(response.text, 'html.parser').find_all('input'):
            if tag['name'] == '__RequestVerificationToken':
                self.token = tag['value']
                break
    
        return self.token

    def get_orgs(self):
        payload = {
            'MIME Type': self.mime_type,
            '__RequestVerificationToken': self.token,
            'Mes': self.months[self.month],
            'Ano': self.year,
            'PesquisarPor': self.search_for,
            'NomePesquisa': self.search_name
        }

        # print(payload)
        response = self.session.post(self.url_orgs, params=payload)
        soup = BeautifulSoup(response.text, 'html.parser')

        org_values = soup.find('table').find_all('td')
        for org, v_bruto, v_patrim, v_total in zip(*[iter(org_values)]*4):
            self.orgs[org.string] = OrgaoRN(org.string,
                                            str(org).split('/')[4].split('?')[0],
                                            v_bruto.float,
                                            v_patrim.float,
                                            v_total.float)

        return self.orgs


    def get_org_employees(self, org):
        # "http://servicos.searh.rn.gov.br/searh/Remuneracao/RemuneracaoPorId/16612356?MesAno=04%2F2019"
        data = {}
        url = self.url_org_data + '/' + org.id
        params = {
            'MesAno': '{}/{}'.format(self.months[self.month], self.year)
        }
        response = self.session.get(url=url, params=params)

        # Get last page
        resp_lines = list(filter(lambda x: len(x) > 0, [l.lstrip() for l in response.text.split('\r\n')]))

        last_page = 1
        for line in resp_lines:
            field = line.split('<a href="/searh/Remuneracao/Paginados?pagina=')
            if len(field) > 1:
                last_page = field[1].split('">')[0]

        print(last_page)

        soup = BeautifulSoup(response.text, 'html.parser')
        print(str(soup.find_all('a')[-2]))

        employee_count = 0
        # Iter over pages
        for pagenum in range(1, int(last_page) + 1):
            data = {}
            url = self.url_org_pag + str(pagenum)
            params = {
                'pagina': pagenum
            }
            response = self.session.get(url=url, params=params)
            resp_lines = list(filter(lambda x: len(x) > 0, [l.lstrip() for l in response.text.split('\r\n')]))

            l = len(resp_lines)
            for n in range(l):
                if resp_lines[n] == '<tbody>': # begin of html table
                    n += 2
                    while n < l:

                        data['Nome do Servidor'] = resp_lines[n][4:-5] # remove '<td>...</td>'
                        data['Cargo/Função'] = resp_lines[n + 1][4:-5]
                        data['Carga Horária'] = resp_lines[n + 2][4:-5]
                        data['Remuneração do Mês'] = float(resp_lines[n + 3][30:-5].replace('.', '').replace(',', '.')
                                                           if resp_lines[n + 3][30:-5] != '' else '0.00')
                        data['Outras Remunerações'] = float(resp_lines[n + 4][30:-5].replace('.', '').replace(',', '.')
                                                           if resp_lines[n + 4][30:-5] != '' else '0.00')
                        data['Previdência'] = float(resp_lines[n + 5][30:-5].replace('.', '').replace(',', '.')
                                                           if resp_lines[n + 5][30:-5] != '' else '0.00')
                        data['Imposto de Reda'] = float(resp_lines[n + 6][30:-5].replace('.', '').replace(',', '.')
                                                           if resp_lines[n + 6][30:-5] != '' else '0.00')
                        data['Redutor ARt.37/CF'] = float(resp_lines[n + 7][30:-5].replace('.', '').replace(',', '.')
                                                           if resp_lines[n + 7][30:-5] != '' else '0.00')
                        data['Outros Descontos'] = float(resp_lines[n + 8][30:-5].replace('.', '').replace(',', '.')
                                                           if resp_lines[n + 8][30:-5] != '' else '0.00')
                        data['Valor Líquido'] = float(resp_lines[n + 9][30:-5].replace('.', '').replace(',', '.')
                                                           if resp_lines[n + 9][30:-5] != '' else '0.00')
                        # print(data)
                        self.orgs[org.name].servidores.append(ServidorRN(
                            data['Nome do Servidor'],
                            data['Cargo/Função'],
                            data['Carga Horária'],
                            data['Remuneração do Mês'],
                            data['Outras Remunerações'],
                            data['Previdência'],
                            data['Imposto de Reda'],
                            data['Redutor ARt.37/CF'],
                            data['Outros Descontos'],
                            data['Valor Líquido'],
                            org.name
                        ))
                        employee_count += 1

                        n += 13 # Jump to next line in html table

                        if resp_lines[n-1] == '</tbody>':
                            break
        print('Found {} {}\'s employees!'.format(employee_count, org.name))

    def get_org(self, s):
        return self.filter_orgs_by_str(s).pop()


    def filter_orgs_by_str(self, s):
        return [self.orgs[org] for org in self.orgs.keys() if s in org]