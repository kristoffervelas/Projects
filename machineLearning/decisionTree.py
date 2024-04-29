import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

#DECISION TREE IS better with high information gain paths (low entropy meaning less variance or difference in each branch)

df = pd.read_csv("titanic.csv")

le = LabelEncoder()
df.Embarked = le.fit_transform(df.Embarked)

sexle = LabelEncoder()
df.Sex = sexle.fit_transform(df.Sex)
inputs = df.drop(['Embarked', 'PassengerId', 'Name', 'Ticket', 'Fare', 'Cabin'], axis='columns')
target = df['Embarked']


from sklearn import tree
from sklearn.model_selection import train_test_split

model = tree.DecisionTreeClassifier()
x_train, x_test, y_train, y_test = train_test_split(inputs, target, test_size=0.2)

model.fit(x_train, y_train)

#print(model.predict(x_test))
print(model.score(x_test, y_test))

print(model.predict([[1,1,0,38.0,1,0]]))

print(inputs)
print(target)
"""

#now do without splitting and using simply input and target datasets

from sklearn import tree

model = tree.DecisionTreeClassifier()

model.fit(inputs, target)
print(model.score(inputs, target))
"""




