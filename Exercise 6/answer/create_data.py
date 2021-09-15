import numpy as np
import pandas as pd

import time
from implementations import all_implementations

# (1) arrays with random integers, which are randomly sorted, 
# (2) arrays that are as large as possible, and
# (3) being able to meaningfully analyse the results. [Note: see the restrictions below.]
data = pd.DataFrame(columns=['qs1', 'qs2', 'qs3', 'qs4', 'qs5', 'merge1', 'partition_sort'], index=np.arange(100))
for i in range(100):
    random_array = np.random.randint(-500,500,1000)
    for sort in all_implementations:
        st = time.time()
        res = sort(random_array)
        en = time.time()
        total = en - st
        data.iloc[i][sort.__name__] = total
    
    
print(data)

data.to_csv('data.csv', index=False)
