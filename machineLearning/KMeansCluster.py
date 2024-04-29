import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#KMEANS CLUSTERING IS FOR UNSUPERVISED LEARNING
"""
how it works:
-start with k number of centroids placing them at random points
-compute distance of every point from centroid and cluster them accordingly
-adjust centroid so they become center of gravity of given cluster
-again recluster every point based on distance with adjusted centroid
-reiterate until data points stop changing cluster
-again adjust centroids

How to find the right amt of k:
-look up elbow method
-basically find the Sum Squared Error for each k, adding the SSE of all subsequent ks
ex: SSE(k=4) = SSE(1) + SSE(2) + SSE(3) + SSE(4)
-once you get the SSE for all ks, plot them on a graph with ks on x-axis and the SSE on the y-axis
-find the "elbow" of the line, self explanatory
-that is the optimal k #
"""

df = pd.read_csv("kMeansIncome.csv")
#print(df.columns)

#plt.scatter(df.Age, df["Income($)"])
#plt.show()

from sklearn.cluster import KMeans
km = KMeans(n_clusters=3)

#fit_predict is the same as km.fit and km.predict
y_predict = km.fit_predict(df[['Age', 'Income($)']])
#output: [1 1 2 2 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 2]
#each # means the cluster that that row belongs to

df['cluster'] = y_predict

#the first time i showed this scatter below, labels had a scaling problem so we fix with minmaxscaler
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
scaler.fit(df[['Income($)']])
df['Income($)'] = scaler.transform(df[['Income($)']])
#now the income column will be in the range of 0-1
#we do the same for age
scaler.fit(df[['Age']])
df['Age'] = scaler.transform(df[['Age']])

#now we use the kmeans again on the scaled data
kmeans = KMeans(n_clusters=3)
ypredict = kmeans.fit_predict(df[['Age', 'Income($)']])
df.drop('cluster', axis='columns', inplace=True) #removing the previous cluster column
df['clusters'] = ypredict
print(df)

#now we separate the 3 types of clusters into 3 diff dataframes
df1 = df[df.clusters == 0]
df2 = df[df.clusters == 1]
df3 = df[df.clusters == 2]

print(kmeans.cluster_centers_) #shows the coords of each centroids
"""
plt.scatter(df1.Age, df1['Income($)'], color='green')
plt.scatter(df2.Age, df2['Income($)'], color='red')
plt.scatter(df3.Age, df3['Income($)'], color='blue')
#plot centroids
#[:,n] means get all the rows in n columns so: [rowStart:rowEnd, colStart:colEnd]
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], color='purple', marker='*', label='centroid')
plt.xlabel('Age')
plt.ylabel('Income')
plt.legend()
plt.show()
"""


#implement elbow method
kRange = range(1, 10)
sse = []
for k in kRange:
    means = KMeans(n_clusters=k)
    means.fit(df[['Age', 'Income($)']])
    sse.append(means.inertia_) #.inertia_ gives the sum squared error

plt.xlabel('k')
plt.ylabel('SSE')
plt.plot(kRange, sse)
plt.show()

#shows that 3 is the elbow thus is the optimal # of k



