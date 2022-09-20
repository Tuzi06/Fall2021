import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
import sys 

monthly_data_labelled = pd.read_csv(sys.argv[1])

X = monthly_data_labelled.loc[:,'tmax-01':'snwd-12'].values
y = monthly_data_labelled['city']

model = make_pipeline(
    StandardScaler(),
    SVC(kernel='linear',C=2.0)
)

X_train, X_valid,y_train,y_valid = train_test_split(X,y)

model.fit(X_train, y_train)

x_unlabled = pd.read_csv(sys.argv[2]).loc[:,'tmax-01':'snwd-12'].values

predictions = model.predict(x_unlabled)
pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)

print('score: ',model.score(X_valid, y_valid))