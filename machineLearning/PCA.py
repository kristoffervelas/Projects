import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
"""
Principal Component Analysis
-Finding which features are crucial to the prediction
Things to keep in mind before using PCA:
1)scale features before applying
2)accuracy might drop
"""

digits = load_digits()
#print(df.keys())
#dict_keys(['data', 'target', 'frame', 'feature_names', 'target_names', 'images', 'DESCR'])
#print(df.data.shape)
#(1797, 64)

df = pd.DataFrame(digits.data, columns=digits.feature_names)

x = df
y = digits.target

#scaling
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaledX = scaler.fit_transform(x)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(scaledX, y, test_size=0.2, random_state=30)

from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(x_train, y_train)
#print(model.score(x_test, y_test))

#now we do PCA
from sklearn.decomposition import PCA
pca = PCA(0.95) #0.95 means retain 95% of useful features
xPCA = pca.fit_transform(x)
#xPCA.shape now returns (1979, 29) meaning it removed some unecessary cols
#print(xPCA.explained_variance_ratio_)

xtrain, xtest, ytrain, ytest = train_test_split(xPCA, y, test_size=0.2, random_state=30)
newmodel = LogisticRegression(max_iter=1000)
newmodel.fit(xtrain, ytrain)
print(newmodel.score(xtest, ytest))



#HOW TO SEE THE MOST IMPORTANT FEATURES!!!!!!

pca2 = PCA(n_components=3)
#n_components being 3 means it will retain the 3 most important features in order of importance in the dataset
#basically its how many important features to keep
new = pca2.fit_transform(x)
print(new)
#print(x)


