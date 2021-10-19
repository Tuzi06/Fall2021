import time
import pandas as pd
import numpy as np
from implementations import all_implementations
# ...

data = pd.DataFrame(columns=['qs1', 'qs2', 'qs3', 'qs4', 'qs5', 'merge1', 'partition_sort'], index=np.arange(10000))
for i in range(10000):
    for sort in all_implementations:
        random_array = np.random.randint(0,1000,100)
        st = time.time()
        res = sort(random_array)
        en = time.time()
        runtime = en - st
        data.iloc[i][sort.__name__] = runtime
    
data.to_csv('data.csv', index=False)