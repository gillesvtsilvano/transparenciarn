from transparencia import TransparenciaRN
import pandas as pd

t = TransparenciaRN('Abril', '2019')

for org in t.orgs:
	print(org, len(org.servidores))
#print(t.get_orgs())
#print(list(t.filter_orgs_by_str('UFRN')))

#itep = t.get_org('ITEP')

