import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

df = pd.read_csv("test_scores.csv")

x = df['math'].values
y = df['cs'].values

reg = linear_model.LinearRegression()
reg.fit(df[['math']].values, df['cs'].values)

def gradient_descent(x, y):
    m_curr = b_curr = 1
    iterations = 100
    n = len(x) #assuming x and y has same len
    learning_rate = 0.1
    #fine tune learning rate and iterations to get best optimization
    #can put a breakpoint based on the cost or if the predictions were correct to a certain threshold

    for i in range(iterations):
        y_predicted = m_curr * x + b_curr
        cost = (1/n) * sum([val**2 for val in (y-y_predicted)])
        m_deriv = -(2/n)*sum(x*(y-y_predicted))
        b_deriv = -(2/n)*sum(y-y_predicted)   
        m_curr = m_curr - learning_rate * m_deriv
        b_curr = b_curr - learning_rate * b_deriv
        print("m {}, b {}, cost {}, iteration {}".format(m_curr,b_curr,cost,i))


#x = np.array([1,2,3,4,5])
#y = np.array([5,7,9,11,13])
#print(x)
#print(y)
gradient_descent(x, y)

print(reg.coef_)
print(reg.intercept_)


