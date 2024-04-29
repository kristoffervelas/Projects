import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import pickle

#LINEAR REGRESSION SINGLE VARIABLE
#ALSO SHOWS HOW TO SAVE MODEL USING PICKLE!!

#difference between pickle and sklearn's joblib
#joblib is better for extensive numpy arrays, essentially the same

df = pd.read_csv("practice.csv")

#plotting the data without regression model
plt.xlabel("year")
plt.ylabel("income")
plt.scatter(df.year, df.income, color='red', marker='+')
#to show just the scatter plot without the line use plt.show()

#create regression model
reg = linear_model.LinearRegression()

#fit data (training the linear regression model using the dataset
reg.fit(df[['year']].values, df.income.values)
#i put .values because without them, it counts the feature names (column labels) which the model does not accept

#to show the line
plt.plot(df.year.values, reg.predict(df[['year']].values), color='blue')
plt.show()

#now the model is ready to predict prices
print(reg.predict([[2023]]))

#show the slope
print(reg.coef_)

#show the intercept
print(reg.intercept_)

#now we can use this to plug into y=mx+b and revengineer how they predicted that value

"""
HYPOTHETICAL

say you have another dataset with one column with a different set of years

#you can read that file
newdf = pd.read_csv("newyears.csv")

#predict the income values for the new years using your fitted regression model
newPrediction = reg.predict(newdf)

#now create new column with the new dataset and assign the predicitons to that one
newdf['newincome'] = newPrediction

#now export it as csv
newdf.to_csv("newpredictions.csv", index=False)
"""

#saving model using pickle
with open('model_pickle', 'wb') as f:
    pickle.dump(reg, f)
#now the model is in the file directory


#to read the model
with open('model_pickle', 'rb') as f:
    mp = pickle.load(f)
#now mp can be used the same as reg
#print(mp)
#print(mp.predict([[5000]]))






