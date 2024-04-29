import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
#handling text data in numeric model:
#1) use integer (or label) encoding where you convert different labels as its own integer value, problem with this is it assumes the order of the numerical values associated with each label

#2 types of categorical variables
"""
1) nominal - where the variables have no connection with each other, no orderings (male, female) (reg, green, blue)
2) ordinal - there is order (high, med, low) (grad, masters, phd)
"""

#ONE HOT ENCODING for nominal variables
#-create a new column for each category(nominal variable) and assign binary value of 1 or 0
#these binary variables are dummy variables

df = pd.read_csv("carprices.csv")

#get the dummy variables from the model column
#.astype is to make it binary values instead of boolean vals
dummies = pd.get_dummies(df.model).astype(np.int8)

#now we concatenate the new columns with dummy vars to the OG dataframe
merged = pd.concat([df, dummies], axis='columns')
#print(merged)

#now since we have the new columns for the dummy variables we can delete the original 'model' column
#apparently we also need to drop one of the columns so it doesnt create a ;dummy variable problem'
#and he says to solve this problem you need to drop any one out of your columns
#dropping the og model col and one dummy col
final = merged.drop(['model', 'Audi A5'], axis='columns')
#print(final) 

reg = LinearRegression()

#now give x and y for training
X = final.drop('price', axis='columns').values
Y = final.price.values

reg.fit(X, Y)

#print(reg.predict([[2800,0,1,0]]))

#print(reg.predict([[3400,0,0,1]]))

#test accuracy
#print(reg.score(X, Y))


"""NOW WE DO THE SAME WITH SKLEARN ONE HOT ENCODING"""
"""
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

dfle = df
dfle.model = le.fit_transform(dfle.model)
#fit_transform takes the label column and returns the labels
#which means this is the easier method as it modifies the labels in the column instead of creating new columns

X = dfle[['model', 'mileage']].values
#print(X)
Y = dfle.price

from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder(categories='auto')
X = ohe.fit_transform(X).toarray()

X = X[:, 1:] #drop the 0th column
print(X)
"""

#SPLITTING DATA BETWEEN TRAIN(80%) and TEST(20%)
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=10)
#random_state parameter makes it so that the data wont change because without it, it changes randomly

#now we train on these datasets
from sklearn.linear_model import LinearRegression

clf = LinearRegression()
clf.fit(x_train, y_train)
print(clf.predict(x_test))
print(y_test)
print(clf.score(x_test, y_test))






