import numpy as np
import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

monthly_data_labelled = pd.read_csv(sys.argv[1])
monthly_data_unlabelled = pd.read_csv(sys.argv[2])

# monthly_data_labelled = pd.read_csv("monthly-data-labelled.csv")
# monthly_data_unlabelled = pd.read_csv("monthly-data-unlabelled.csv")

X = monthly_data_labelled.loc[:,'tmax-01':'snwd-12'].values
y=  monthly_data_labelled['city'].values
X_train, X_valid, y_train, y_valid = train_test_split(X, y)

svm_model = make_pipeline(StandardScaler(), SVC(kernel='linear', C=0.1))
svm_model.fit(X_train, y_train)
#print(svm_model.score(X_valid, y_valid))

# nb_model = make_pipeline(StandardScaler(), GaussianNB())
# nb_model.fit(X_train, y_train)
# print(nb_model.score(X_valid, y_valid))

# t1_model = make_pipeline(StandardScaler(), DecisionTreeClassifier(max_depth=15))
# t1_model.fit(X_train, y_train)
# print(t1_model.score(X_valid, y_valid))

# t2_model = make_pipeline(StandardScaler(), DecisionTreeClassifier(min_samples_leaf=10))
# t2_model.fit(X_train, y_train)
# print(t2_model.score(X_valid, y_valid))

# model = VotingClassifier([
#     #('nb', GaussianNB()),
#     #('knn', KNeighborsClassifier(5)),
#     ('svm', SVC(kernel='linear', C=0.1)),
#     #('tree1', DecisionTreeClassifier(max_depth=4)),
#     #('tree2', DecisionTreeClassifier(min_samples_leaf=10)),
# ])
# model.fit(X_train, y_train)
# print(model.score(X_valid, y_valid))

X_unlabelled = monthly_data_unlabelled.loc[:,'tmax-01':'snwd-12'].values
predictions = svm_model.predict(X_unlabelled)

print('Model Score is ',svm_model.score(X_valid, y_valid))

pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)


