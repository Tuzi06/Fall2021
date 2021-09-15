import numpy as np

data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']

sum = np.sum(totals,1)
print(np.argmin(sum));