import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Naive Bayes Classifiers:

1)Bernoulli Naive Bayes - assumes that all features are binary

2)Multinomial Naive Bayes - used with discrete data(ex: 1-5)

3)Gaussian Naive Bayes - used when all features are continuous, or varies
"""

df = pd.read_csv("spamNaive.csv")

#category column is txt we need to convert to #
df['spam'] = df['Category'].apply(lambda x:1 if x == 'spam' else 0)
df = df.drop('Category', axis='columns')
#print(df)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(df.Message, df.spam, test_size=0.25)

#now we get the unique words from each phrase
from sklearn.feature_extraction.text import CountVectorizer
v = CountVectorizer()
x_train_count = v.fit_transform(x_train.values)
#print(x_train_count.toarray()[:3])




from sklearn.naive_bayes import MultinomialNB

model = MultinomialNB()
model.fit(x_train_count, y_train)

emails = ['Hey kris, can we get together to watch football game tomorrow?', 'Up to 20% discount on parking, exclusive offer just for you']

emails_count = v.transform(emails)
#print(model.predict(emails_count))

x_test_count = v.transform(x_test)
#print(model.score(x_test_count, y_test))


#using pipeline to write all the above in shorter code

from sklearn.pipeline import Pipeline
clf = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('nb', MultinomialNB())
])

clf.fit(x_train, y_train)
print(clf.score(x_test, y_test))


