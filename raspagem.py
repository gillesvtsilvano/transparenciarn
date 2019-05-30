from transparencia import TransparenciaRN
from pandas import DataFrame


"""
Dataset: rn_abril_2019.csv

Nome do Servidor	Órgao	Cargo/Função	Carga Horária	Remuneração do Mês	Outras Remunerações(*)	
Previdência	Imposto de Renda	Redutor Art.37/CF	Outros Descontos	Valor Líquido
"""
if __name__ == "__main__":
	t = TransparenciaRN('Abril', '2019') #2491998

	#for _, org in t.orgs.items():
	#	print(org, len(org.servidores))

	#itep = t.get_org('ITEP')

	column_names = [
		'Nome do Servidor',
		'Orgão',
		'Cargo/Função',
		'Carga Horária',
		'Remuneração do Mês',
		'Outras Remunerações',
		'Previdência',
		'Imposto de Renda',
		'Redutor Art.37/CF',
		'Outros Descontos',
		'Valor Líquido'
	]

	serv_list = []

	for _,org in t.orgs.items():
		for servidor in org.servidores:
			s = dict()
			s['Nome do Servidor'] = servidor.nome
			s['Orgão'] = servidor.orgao
			s['Cargo/Função'] = servidor.cargo
			print(servidor.nome, servidor.orgao, servidor.cargo)
			s['Carga Horária'] = servidor.ch
			s['Remuneração do Mês'] = servidor.remuneracao_base
			s['Outras Remunerações'] = servidor.remuneracao_outras
			s['Previdência'] = servidor.previdencia
			s['Imposto de Renda'] = servidor.ir
			s['Redutor Art.37/CF'] = servidor.redutor
			s['Outros Descontos'] = servidor.descontos_outros
			s['Valor Líquido'] = servidor.liquido
			serv_list.append(s)


	df = DataFrame(serv_list, columns=column_names)

	df.to_csv("04_2019.csv")
