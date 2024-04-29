import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
How K-Fold Cross Validation works:

K-Fold is for evaluating a models general performance

-divide dataset into folds
-there will be one iteration for each fold where fold[iteration] will be used as the test while everything else is train
-now you take the average  of each iteration to get the ave score
"""

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

digits = load_digits()

#NOW WE USE K-FOLD
from sklearn.model_selection import KFold

kf = KFold(n_splits=3)

def get_score(model, x_train, x_test, y_train, y_test):
    model.fit(x_train, y_train)
    return model.score(x_test, y_test)

from sklearn.model_selection import StratifiedKFold
#stratified k fold divides each category in a uniform way
folds = StratifiedKFold(n_splits=3)

#now prepare the score arrays
scores_log = []
scores_svm = []
scores_rf = []

for train_index, test_index in kf.split(digits.data):
    x_train, x_test, y_train, y_test = digits.data[train_index], digits.data[test_index], digits.target[train_index], digits.target[test_index]
    regScore = get_score(LogisticRegression(), x_train, x_test, y_train, y_test)
    svmScore = get_score(SVC(), x_train, x_test, y_train, y_test)
    rfScore = get_score(RandomForestClassifier(), x_train, x_test, y_train, y_test)

    scores_log.append(regScore)
    scores_svm.append(svmScore)
    scores_rf.append(rfScore)

#print(scores_log)
#print(scores_svm)
#print(scores_rf)

#NOW INSTEAD OF DOING ALL THAT FOR LOOPING YOU CAN DO THIS INSTEAD
from sklearn.model_selection import cross_val_score

print(cross_val_score(LogisticRegression(), digits.data, digits.target))
print(cross_val_score(SVC(), digits.data, digits.target))
print(cross_val_score(RandomForestClassifier(), digits.data, digits.target))





