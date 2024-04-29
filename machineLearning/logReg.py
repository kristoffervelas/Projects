import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

"""MULTICLASS CLASSIFICATION"""

from sklearn.datasets import load_digits
#1797 8x8 images of handwritted imgs ^^^

digits = load_digits()
#dir(digits)

#print individual elements from the dataset

#plt.gray()
#for i in range(5):
#    plt.matshow(digits.images[i])
#    plt.show()

x_train, x_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.2)

logReg = LogisticRegression()
logReg.fit(x_train, y_train)

#plt.matshow(digits.images[20])
#plt.show()
#print(logReg.predict([digits.data[20]]))
#print(logReg.score(x_test, y_test))
#works very well

y_predicted = logReg.predict(x_test)

from sklearn.metrics import confusion_matrix
#check the accuracy data of the model predictions
cm = confusion_matrix(y_test, y_predicted)
print(cm)
#x axis is predicted and y axis is truth


"""BINARY CLASSIFICATION"""

"""
#Squishing the linear equation into sigmoid function to come up with a value between 0 n 1
#linear eq plugged into the sigmoid function
#1 / (1 + e^(mx+b))

df = pd.read_csv("insurance_data.csv")

plt.scatter(df.age, df.bought_insurance, marker='+', color='red')
#plt.show()

#split data into test and train
x_train, x_test, y_train, y_test = train_test_split(df[['age']].values, df.bought_insurance.values, train_size=0.9)

#create model and fit
log = LogisticRegression()
log.fit(x_train, y_train)

print(log.predict_proba(x_test))

#predict the test dataset
print(log.predict(x_test))

print(log.score(x_test, y_test))
#100%accuracy
"""

