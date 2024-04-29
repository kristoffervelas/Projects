import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
P(A|B) = Probability of A given than B has alrdy occured (conditional probability)
formula = P(A|B) = (P(B|A) * P(A)) / P(B)

called naive bayes because we make naive assumption that all features are independent of each other
"""
df = pd.read_csv("titanicNaive.csv")
df.drop(['PassengerId', 'Name', 'SibSp', 'Parch', 'Ticket', 'Cabin', 'Embarked'], axis='columns', inplace=True)

target = df.Survived
inputs = df.drop('Survived', axis='columns')

#we need to use OHE on Sex column
dummies = pd.get_dummies(inputs.Sex).astype(np.int16)
inputs = pd.concat([inputs, dummies], axis='columns')
inputs = inputs.drop('Sex', axis='columns')

#were gonna check for any NaN values
#print(inputs.columns[inputs.isna().any()])
#says that Age col have NaN
#so we replace them with the mean of the column

inputs.Age = inputs.Age.fillna(inputs.Age.mean())

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(inputs, target, test_size=0.2)

#now we use naive bayes

from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model.fit(x_train, y_train)

print(model.score(x_test, y_test))
#print(model.predict(x_test))
#print(model.predict([[2, 29.0, 7.6, 1, 0]]))
#print(model.predict_proba(x_test[:10]))
