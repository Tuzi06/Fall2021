import numpy as np
import pandas as pd
from scipy import stats

dog_rates = pd.read_csv('dog_rates_tweets.csv',parse_dates=[1])

rate_data= dog_rates.text.str.extract(r'(\d+(\.\d+)?)/10')
rate= rate_data[0].dropna()

rate = pd.to_numeric(rate)
rate = rate[rate<=25]
dog_rates['rating']= rate
data = dog_rates.loc[rate.index]

def to_timestamp(d):
    return d.timestamp()

data['timestamp'] = data['created_at'].apply(to_timestamp)

fit = stats.linregress(data['timestamp'],data['rating'])
data['prediction'] = data['timestamp']*fit.slope + fit.intercept

