import numpy as np
import pandas as pd
from sklearn import svm, datasets

iris = datasets.load_iris()

df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['flower'] = iris.target
df['flower'] = df['flower'].apply(lambda x: iris.target_names[x])

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3)

#the SVC model has parameters that are crucial to prediction such as kernel and C

#we will test out the results with different parameters
from sklearn.model_selection import cross_val_score

kernels = ['rbf', 'linear']
C = [1, 10, 20]
avg_scores = {}

for kval in kernels:
    for cval in C:
        cv_scores = cross_val_score(svm.SVC(kernel=kval, C=cval, gamma='auto'), iris.data, iris.target, cv=5)
        avg_scores[kval + '_' + str(cval)] = np.average(cv_scores)

#print(avg_scores) shows best parameter matching

#WE CAN DO ALL THAT IN ONE LINE OF CODE ^^^

from sklearn.model_selection import GridSearchCV

clf = GridSearchCV(svm.SVC(gamma='auto'), {
    'C': [1, 10, 20],
    'kernel': ['rbf', 'linear']
}, cv=5, return_train_score=False)

clf.fit(iris.data, iris.target)

result = pd.DataFrame(clf.cv_results_)
#print(result)
#lets trim down the reulsts
print(result[['param_C', 'param_kernel', 'mean_test_score']])
print(clf.best_score_)
print(clf.best_params_)


