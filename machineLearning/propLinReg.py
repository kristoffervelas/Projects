import numpy as np
import matplotlib.pyplot as plt

#y = mx + b

#Function to calculate m and b
def linear_regression(x, y):
    #ordinary least squares method
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sum((x - x_mean) ** 2)
    m = numerator / denominator
    b = y_mean - (m * x_mean)
    return m, b

#function to calculate prediction
def predict(x, m, b):
   #the Y
   return m * x + b

#function to calculate RMSE (root mean squared error / measure models performance)
def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

x = np.array([7,8,10, 12, 15, 18])
y = np.array([9,10,12,13,16,20])

#train model
m, b = linear_regression(x, y)

#make pred
predictions = predict(x, m, b)
error = rmse(y, predictions)

print("Slope(m): ", m)
print("Intercept(b): ", b)
print("Predictions: ", predictions)
print("RMSE: ", error)

#now visualize
plt.scatter(x, y, color='blue', label='Data Points')
plt.plot(x, predictions, color='red', label='Regression Line')
plt.xlabel('Independent Variable X')
plt.ylabel('Dependent Variable Y')
plt.title("Linear Regression Model")
plt.legend()
plt.show()



