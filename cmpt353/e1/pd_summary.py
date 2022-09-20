import pandas as pd

totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])

total_city = totals.sum(1)
print('City with lowest total precipitation:\n',total_city.idxmin())

total_part =totals.sum(0)
totals_ob = counts.sum(0)
print ('Average precipitation in each city:\n',total_part / totals_ob)

total_part =totals.sum(1)
totals_ob = counts.sum(1)
print ('Quarterly precipitation totals:\n',total_part / totals_ob)