#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


filename1 = sys.argv[1]
filename2 = sys.argv[2]


# plot1

# In[3]:


data1=pd.read_csv(filename1, sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])
data1_decreasing_view= data1.sort_values(by='views', ascending=False)


# plot2

# In[4]:


data2=pd.read_csv(filename2, sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])


# In[5]:


copy_data=data1#get the two series into the same DataFrame
copy_data=copy_data.rename(columns={"views": "views1"})
copy_data['views2']=data2['views']


# In[13]:


plt.figure(figsize=(10,5)) # change the size to something sensible
plt.subplot(1, 2, 1) # subplots in 1 row, 2 columns, select the first
plt.plot(data1_decreasing_view['views'].values) # build plot 1
plt.title('Popularity Distribution')
plt.ylabel('Views')
plt.xlabel('Rank')

plt.subplot(1, 2, 2) # ... and then select the second
plt.xscale('log')
plt.yscale('log')
plt.plot(copy_data['views1'], copy_data['views2'],'b.',markersize=4)
plt.title('Hourly Correlation')
plt.ylabel('Hours 2 views')
plt.xlabel('Hour 1 views')
plt.savefig('wikipedia.png')


# In[ ]:




