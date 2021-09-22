import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename1 = sys.argv[1]
filename2 = sys.argv[2]

file2 = pd.read_csv(filename2, sep=' ', header=None, index_col=1,names=['lang', 'page', 'views', 'bytes'])
file1 = pd.read_csv(filename1, sep=' ', header=None, index_col=1,names=['lang', 'page', 'views', 'bytes'])

sort1 = file1. sort_values(by='views',ascending = False)
print(file1)
print (file2)

copy = file1.copy()
copy['views2'] = file2['views'] 
print (copy)


plt.figure(figsize=(10, 5)) # change the size to something sensible
plt.subplot(1, 2, 1) # subplots in 1 row, 2 columns, select the first
plt.plot(sort1['views'].values) # build plot 1

plt.subplot(1, 2, 2) # ... and then select the second
plt.plot(copy['views'],copy['views2'],'b.',alpha=0.5) # build plot 2
plt.xscale("log", nonposx ='clip') 
plt.yscale("log", nonposy ='clip') 

plt.show()