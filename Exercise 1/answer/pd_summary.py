#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])


# In[3]:


sum_pre = totals.sum(axis=1)
print("City with lowest total precipitation:")
print(sum_pre.idxmin())


# In[4]:


ave_month=totals.sum(axis=0)/counts.sum(axis=0)
print("Average precipitation in each month:")
print(ave_month)


# In[5]:


ave_city=totals.sum(axis=1)/counts.sum(axis=1)
print("Average precipitation in each city:")
print(ave_city)

