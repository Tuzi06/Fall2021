import numpy as np

data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']

sum_city = np.sum(totals,1)
print('Row with lowest total precipitation: \n',np.argmin(sum_city))

total_part =np.sum(totals,0)
totals_ob = np.sum(counts,0)
print ('Average precipitation in each month: \n',total_part / totals_ob)

total_part =np.sum(totals,1)
totals_ob = np.sum(counts,1)
print ('Average precipitation in each city:\n',total_part / totals_ob)

total_reshape = np.reshape(totals,(4*len(totals),3))
total_quad=np.sum(total_reshape,1)
total_quad=np.reshape(total_quad,(len(totals),4))
print('Quarterly precipitation totals:\n',total_quad)