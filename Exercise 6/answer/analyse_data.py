import sys
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data_file = sys.argv[1]
#data_file ="data.csv"
data = pd.read_csv(data_file)

# ANOVA test, to see if any of the groups differ
anova = stats.f_oneway(data.iloc[:,0], data.iloc[:,1], data.iloc[:,2], data.iloc[:,3], data.iloc[:,4], data.iloc[:,5], data.iloc[:,6])
print(anova)
print(anova.pvalue)
#We conclude that yes: with p<0.5 , there is a difference between the means of the groups.


# Post Hoc Analysis
data_melt = pd.melt(data)
posthoc = pairwise_tukeyhsd(data_melt['value'], data_melt['variable'], alpha=0.05)
print(posthoc)
fig = posthoc.plot_simultaneous()


print(data.mean())