import requests
from orgao import OrgaoRN
from servidor import ServidorRN




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
        print('Ok')

        print('Acquiring token access...', end='')
        self.get_token()
        print('Ok')
        print('Finding organizations...', end='')
        self.get_orgs()
        print('Ok')
        print('Finding employees...', end='')
        if not orgs:
            for _,v in self.orgs.items():

                print(v.name + '...', end=''),
                self.get_org_employees(v)
                print('Ok')
        else:
            for org_name in orgs:
                org = self.get_org(org_name)
                self.get_org_employees(org)


    def get_token(self):
        response = self.session.get(self.url_base)
        self.token = response.text.split('__RequestVerificationToken')[1].split('value=')[1].split(' ')[0][1:-1]
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
        response_list = list(filter(lambda x: len(x) > 0, [l.lstrip() for l in response.text.split('\r\n')]))
        l = len(response_list)
        for idx in range(l):
            counter = -1
            org_name = ''
            org_id = ''
            org_bruto = ''
            org_patronal = ''
            org_total = ''

            split = response_list[idx].split('<td><a href="/searh/Remuneracao/RemuneracaoPorId')
            if len(split) > 1:
                for s in filter(lambda x: x != '', split):
                    org_name = s.split('>')[1].split('</a>')[0][:-3]
                    org_id = s.split('/')[1].split('?')[0]
                    org_bruto = response_list[idx+1][30:-5]
                    org_patronal = response_list[idx+2][30:-5]
                    org_total = response_list[idx+3][30:-5]
                    o = OrgaoRN(org_name, org_id, org_bruto, org_patronal, org_total)
                    self.orgs[org_name] = o
                    idx += 6
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

        # Iter over pages
        for pagenum in range(1, int(last_page) + 1):
        #for pagenum in range(1, 2):
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
                        data['Remuneração do Mês'] = resp_lines[n + 3][30:-5]
                        data['Outras Remunerações'] = resp_lines[n + 4][30:-5]
                        data['Previdência'] = resp_lines[n + 5][30:-5]
                        data['Imposto de Reda'] = resp_lines[n + 6][30:-5]
                        data['Redutor ARt.37/CF'] = resp_lines[n + 7][30:-5]
                        data['Outros Descontos'] = resp_lines[n + 8][30:-5]
                        data['Valor Líquido'] = resp_lines[n + 9][30:-5]
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

                        n += 13 # Jump to next line in html table

                        if resp_lines[n-1] == '</tbody>':
                            break

    def get_org(self, s):
        return self.filter_orgs_by_str(s).pop()


    def filter_orgs_by_str(self, s):
        return [self.orgs[org] for org in self.orgs.keys() if s in org]
