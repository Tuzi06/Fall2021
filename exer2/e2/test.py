import numpy as np
import pandas as pd
import re

dog_rates = pd.read_csv('dog_rates_tweets.csv',sep = ',',index_col =0)
print(dog_rates['text'].dtype)

dog_rates['text'].dtype = np.str_


dog_rates['rating'] = re.match(r'(\d+(\.\d+)?)/10',dog_rates['text'])



m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
m=m.group(0)  
print(m)