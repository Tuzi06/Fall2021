import pandas as pd 
from scipy import stats
import matplotlib.pyplot as plt

data = pd.read_csv('data.csv')
plt.plot(data,'.b')
plt.show()
print(data)