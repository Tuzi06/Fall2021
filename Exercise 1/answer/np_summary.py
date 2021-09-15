import numpy as np

data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']


sum_pre= np.sum(totals, axis=1)  
print("Row with lowest total precipitation:",)
print(np.argmin(sum_pre))

ave_month = np.sum(totals, axis=0) / np.sum(counts, axis=0)
print("Average precipitation in each month:")
print(ave_month)

ave_city=sum_pre/np.sum(counts,axis=1)
print("Average precipitation in each city:")
print(ave_city)

total_qua= np.reshape(totals, (4*len(totals), 3))
total_qua_city =  np.sum(total_qua, axis=1)
total_qua_city.shape = (len(totals), 4)
print("Quarterly precipitation totals:")
print (total_qua_city)
