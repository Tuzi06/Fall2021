import pandas as pd 
from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv('data.csv')

anova = stats.f_oneway(data['qs1'], data['qs2'], data['qs3'], data['qs4'], data['qs5'], data['merge1'], data['partition_sort']).pvalue

melt = pd.melt(data)
# print(melt)
posthoc = pairwise_tukeyhsd(melt['value'],melt['variable'],alpha =0.05)
# print(posthoc)

fig = posthoc.plot_simultaneous()
