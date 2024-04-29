import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, QuantileTransformer

#Look into imputer sklearn
#QuantileTransformer is alternative to StandardScaler
#Polynomial features is another scaling alternative to these 2, it creates nonlinearity

df1 = pd.read_csv("drawndata1.csv")
df2 = pd.read_csv("drawndata2.csv")

x1 = df1[['x', 'y']].values
y1 = df1['z'] == 'a'

x2 = df2[['x', 'y']].values
y2 = df2['z'] == 'a'

#show drawndata2
#plt.scatter(x2[:, 0], x2[:, 1], c=y2)
#plt.show()


#show drawndata1
#plt.scatter(x1[:, 0], x1[:, 1], c=y1)
#plt.show()

#after using standard scaler, it didnt really do anything to fix the outliers
#we try quantileTransformer

newX = QuantileTransformer(n_quantiles=100).fit_transform(x1)
#plt.scatter(newX[:,0], newX[:,1], c=y1)
#plt.show()


#now we apply quantile transformer into a pipeline

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("scale", QuantileTransformer(n_quantiles=100)),
    ("model", LogisticRegression())
])

pred = pipe.fit(x2, y2).predict(x2)
plt.scatter(x2[:,0], x2[:,1], c=pred)
plt.show()


