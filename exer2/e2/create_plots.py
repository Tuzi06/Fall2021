import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename1 = sys.argv[1]
filename2 = sys.argv[2]

file1 = pd.read_csv(filename1, sep=' ', header=None, index_col=1,names=['lang', 'page', 'views', 'bytes'])
file2 = pd.read_csv(filename2, sep=' ', header=None, index_col=1,names=['lang', 'page', 'views2', 'bytes'])

sort1 = file1. sort_values(by='views',ascending = False)

copy = pd.concat([file1,file2],axis=1)
print(copy)

plt.figure(figsize=(10, 5)) # change the size to something sensible
plt.subplot(1, 2, 1) # subplots in 1 row, 2 columns, select the first
plt.plot(sort1['views'].values) # build plot 1
plt.title('Distribution of Views')
plt.xlabel('sorted Wikipedia pages from highest number of views to lowest')
plt.ylabel('views')

plt.subplot(1, 2, 2) # ... and then select the second
plt.plot(copy['views'],copy['views2'],'b.',alpha=1) # build plot 2
plt.xscale('log')
plt.yscale('log') 
plt.title('Hourly Views')
plt.xlabel('views at 12:00')
plt.ylabel('views at 13:00')

plt.savefig('wikipedia.png')

plt.show()