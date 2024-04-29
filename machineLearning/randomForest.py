import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

"""
how this works

-divide dataset into random sets
-now for each one of them create a decision tree
-now make a prediction for all of them
-the majority vote will be your prediction
"""
from sklearn.datasets import load_digits
digits = load_digits()

#print(dir(digits))
#[DESCR, data, images, target, target_names]

"""
plt.gray()
for i in range(4):
    plt.matshow(digits.images[i])
    plt.show()
"""

df = pd.DataFrame(digits.data)

#append the target values into another column
df['target'] = digits.target

x_train, x_test, y_train, y_test = train_test_split(df.drop(['target'], axis='columns'), df.target, test_size=0.2)

#import classifier
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=30) #n_estimators is the # of trees, the more the more accurate
#print(model)
model.fit(x_train, y_train)

#normal prediction
#print(model.predict(x_test))
#print(model.score(x_test, y_test))

#create a confusion matrix for the predictin
from sklearn.metrics import confusion_matrix

y_predict = model.predict(x_test)
cm = confusion_matrix(y_test, y_predict)
print(cm)



