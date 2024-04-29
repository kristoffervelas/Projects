import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
K Nearest Neighbor
How it works:
say k = 10
take 10 nearest points and the majority is the class

*for highsly structures data use low K, for noisy data use higher K

"""

from sklearn.datasets import load_iris
iris = load_iris()

df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target

df0 = df[:50]
df1 = df[50:100]
df2 = df[100:]

#plt.xlabel('Sepal length')
#plt.ylabel('Sepal width')
#plt.scatter(df0['sepal length (cm)'], df0['sepal width (cm)'], color='green', marker='+')
#plt.scatter(df1['sepal length (cm)'], df1['sepal width (cm)'], color='blue', marker='.')
#plt.show()
#print(df.columns)
inputs = df.drop(['target'], axis='columns')
out = df.target

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(inputs, out, test_size=0.2, random_state=1)

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=10)
knn.fit(x_train, y_train)
print(knn.score(x_test, y_test))

from sklearn.metrics import confusion_matrix

y_pred = knn.predict(x_test)
cm = confusion_matrix(y_test, y_pred)
print(cm)

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))


