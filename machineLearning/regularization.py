import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

"""
Regularization is for when the model is overfitter or underfitted
-It is used to calibrate the linear regression models in order to minimize the adjusted loss function and prevent overfitting
or underfitting

2 types of regularizations

Ridge Regression (L2)
-modifies the overfitted or underfitted models by adding the penalty equivalent to the sum of the squares of the magnitude of
coefficients
-useful when we have many variables with relatively smaller data samples

Lasso Regularization (L1)
-modifies the overfitted or underfitted models by adding the penalty equivalent to the sum of the absolute values of coefficients
-preferred when we are fitting a linear model with fewer variables

"""

df = pd.read_csv("housing.csv")

colsToUse = ['Suburb', 'Rooms', 'Type', 'Method', 'SellerG', 'Regionname', 'Propertycount', 'Distance', 'CouncilArea', 'Bedroom2', 'Bathroom', 'Car', 'Landsize', 'BuildingArea', 'Price']
df = df[colsToUse]


#first we have to fill the zeros
colsToFill = ['Propertycount', 'Distance', 'Bedroom2', 'Bathroom', 'Car']
df[colsToFill] = df[colsToFill].fillna(0)
df['Landsize'] = df['Landsize'].fillna(df.Landsize.mean())
df['BuildingArea'] = df['BuildingArea'].fillna(df.BuildingArea.mean())
#print(df.isna().sum())
df.dropna(inplace=True)

#now we deal with dummy variables
df = pd.get_dummies(df, drop_first=True).astype(np.int16)

inputs = df.drop('Price', axis=1)
target = df['Price']

x_train, x_test, y_train, y_test = train_test_split(inputs, target, test_size = 0.3)

print(df)

model = LinearRegression()
model.fit(x_train, y_train)

print(model.score(x_test, y_test))
print(model.score(x_train, y_train))
#so model is clearly overfitted so we will use L1 regularization
#L1 Regularization
from sklearn.linear_model import Lasso
lasso_reg = Lasso(alpha=50, max_iter=100, tol=0.1)
lasso_reg.fit(x_train, y_train)
print(lasso_reg.score(x_test, y_test))

#L2 Regularization
from sklearn.linear_model import Ridge
ridge = Ridge(alpha=50, max_iter=100, tol=0.1)
ridge.fit(x_train, y_train)

print(ridge.score(x_test, y_test))

