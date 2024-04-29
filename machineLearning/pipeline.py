import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
import math
from sklearn.datasets import load_diabetes
from sklearn.model_selection import GridSearchCV

#tutorial for pipeline and gridsearchcv
#Pipeline allows you to chain processing steps sequentially in one go
#GridSearchCV is good for hyperparam tuning

#you can have pipeline inside pipeline

x, y = load_diabetes(return_X_y = True)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

pipe = Pipeline([
    ("scale", StandardScaler()),
    ("model", KNeighborsRegressor())
])

#print(pipe.get_params())

#we get model_n_neighbors from pipe.get_params()
model = GridSearchCV(estimator=pipe,
             param_grid={'model__n_neighbors':[1,2,3,4,5,6,7,8,9,10]},
             cv=3)

#assuming that we didn't do the train_test_split
model.fit(x, y)
print(model.score(x_test, y_test))
#print(pd.DataFrame(model.cv_results_))

#pipe.fit(x_train, y_train)
#pred = pipe.predict(x_test)
#plt.scatter(pred, y_test)
#plt.show()
#print(pipe.score(x_test, y_test))


