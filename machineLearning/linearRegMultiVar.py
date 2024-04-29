import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
import math


df = pd.read_csv("homeprices.csv")

#dataset has a NaN value so we will handle it by replacing with the median of its column
#was returning 3.5, we want full digits so we use floor
median_bedrooms = math.floor(df.bedrooms.median())

#now replace the NaN values in the column with the median
df.bedrooms = df.bedrooms.fillna(median_bedrooms)

#now we create and fit the model
reg = linear_model.LinearRegression()
reg.fit(df[['area', 'bedrooms', 'age']].values, df.price.values)

#now get coefficients(slope)
#print(reg.coef_)
#intercept
#print(reg.intercept_)

#now we predict
print(reg.predict([[2500, 4, 5]]))


