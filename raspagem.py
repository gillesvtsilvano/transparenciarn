from transparencia import TransparenciaRN
import pandas as pd


"""
Dataset: rn_abril_2019.csv

Nome do Servidor	Órgao	Cargo/Função	Carga Horária	Remuneração do Mês	Outras Remunerações(*)	
Previdência	Imposto de Renda	Redutor Art.37/CF	Outros Descontos	Valor Líquido
"""
if __name__ == "__main__":
	t = TransparenciaRN('Abril', '2019', ['ITEP'])

	#for _, org in t.orgs.items():
	#	print(org, len(org.servidores))

	itep = t.get_org('ITEP')
	print(itep.servidores)


