import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#SUPPORT VECTOR MACHINES
"""
-SVM draws a hyper plane in n dimensional space such that it maximizes margin between classification groups
For 2d:
-The way they find the best line is to find the best line with the highest margin (margin is the distance of n closest points to the line), higher margin means they are better separated
"""

from sklearn.datasets import load_iris

iris = load_iris()

#print(dir(iris)) #shows the feature labels
#['DESCR', 'data', 'data_module', 'feature_names', 'filename', 'frame', 'target', 'target_names']

df = pd.DataFrame(iris.data, columns=iris.feature_names)
#appending the target column
df['target'] = iris.target

#print(df.head())
#print(df[df.target == 1].head())

df['flower_name'] = df.target.apply(lambda x: iris.target_names[x])
#basically means whatever target is(0,1,2) append the iris.target_names with the index of the initial target value into the new column'flower_name'
#print(df.head())

#now separate the three species into three dataframes

df0 = df[df.target == 0]
df1 = df[df.target == 1]
df2 = df[df.target == 2]

#now we plot
plt.xlabel('sepal length (cm)')
plt.ylabel('sepal width (cm)')
plt.scatter(df0['sepal length (cm)'], df0['sepal width (cm)'], color='red', marker='+')
plt.scatter(df1['sepal length (cm)'], df1['sepal width (cm)'], color='blue', marker='.')
#plt.show()

plt.xlabel('petal length (cm)')
plt.ylabel('petal width (cm)')
plt.scatter(df0['petal length (cm)'], df0['petal width (cm)'], color='red', marker='+')
plt.scatter(df1['petal length (cm)'], df1['petal width (cm)'], color='blue', marker='.')

#plt.show()

#now we remove unecessary columns from the dataset
X = df.drop(['target', 'flower_name'], axis='columns')
Y = df.target

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

from sklearn.svm import SVC

model = SVC()
model.fit(x_train, y_train)
print(model.predict(x_test))
print(model.score(x_test, y_test))




