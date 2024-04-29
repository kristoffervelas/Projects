#processes on matrix
#find good matching features on matrix
#create a convolution layer on the features
#relu on new layer
#then a pooling layer on the output of conv layer

#for now use "X" on a 9x9 matrix

import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt

matrix = [[-1,-1,-1,-1,-1,-1,-1,-1,-1],
          [-1,1,-1,-1,-1,-1,-1,1,-1],
          [-1,-1,1,-1,-1,-1,1,-1,-1],
          [-1,-1,-1,1,-1,1,-1,-1,-1],
          [-1,-1,-1,-1,1,-1,-1,-1,-1],
          [-1,-1,-1,1,-1,1,-1,-1,-1],
          [-1,-1,1,-1,-1,-1,1,-1,-1],
          [-1,1,-1,-1,-1,-1,-1,1,-1],
          [-1,-1,-1,-1,-1,-1,-1,-1,-1]]

downRight = [[1,-1,-1],
            [-1,1,-1],
            [-1,-1,1]]
upRight = [[-1,-1,1],
            [-1,1,-1],
            [1,-1,-1]]
cross = [[1,-1,1],
         [-1,1,-1],
         [1,-1,1]]

convLayer1 = [] #this is the output of downRight convo layer
convLayer2 = [] #this is the output of upRight convo layer
convLayer3 = [] #this is the output of cross convo layer

def product(pattern, kernel):
    output = []
    for row in range(len(pattern)):
        for col in range(len(pattern[0])):
            output.append(pattern[row][col] * kernel[row][col])
    return sum(output) / 9


for row in range(2, len(matrix)):
    
    #gather everything 3 and below for row and col

    tempRow1 = []
    tempRow2 = []
    tempRow3 = []

    for col in range(2, len(matrix[0])):
        #gather the kernel window
        #do product on each pattern and append to corresponding convLayer array
        window = [[],[],[]]
        for z in range(col-2, col+1):
            window[0].append(matrix[row][z]) #curr row
            window[1].append(matrix[row-1][z]) #one row down
            window[2].append(matrix[row-2][z]) #two rows down

        tempRow1.append(product(downRight, window))
        tempRow2.append(product(upRight, window))
        tempRow3.append(product(cross, window))

    #append tempRow to corr layer
    convLayer1.append(tempRow1)
    convLayer2.append(tempRow2)
    convLayer3.append(tempRow3)

#format the output layers
for i in range(len(convLayer1)):
    for j in range(len(convLayer1[0])):
        convLayer1[i][j] = float("{:.2f}".format(convLayer1[i][j]))
        convLayer2[i][j] = float("{:.2f}".format(convLayer2[i][j]))
        convLayer3[i][j] = float("{:.2f}".format(convLayer3[i][j]))

"""
for i in convLayer1:
    print(i)
print("\n")
for i in convLayer2:
    print(i)
print("\n")
for i in convLayer3:
    print(i)
print("\n")
"""


#SHOW HEATMAP
"""
first = sn.heatmap(data=convLayer1, annot=True)
plt.show()
second = sn.heatmap(data=convLayer2, annot=True)
plt.show()
third = sn.heatmap(data=convLayer3, annot=True)
plt.show()
"""     

#NOW DO POOLING LAYER ON THE CONV LAYERS

def pooling(trix):
    #add one row and col of 0s
    matrix = trix
    if len(matrix[0])%2!=0:
        for row in matrix:
            row.append(0.0)
    if len(matrix)%2!=0:
        matrix.append([0.0 for i in range(len(matrix[0]))])

    outputLayer = []

    for row in range(1, len(matrix), 2):
        layer = []        
        for col in range(1, len(matrix[0]), 2):
            temp = [matrix[row][col], matrix[row-1][col], matrix[row][col-1], matrix[row-1][col-1]]
            layer.append(max(temp))
        outputLayer.append(layer)

    return outputLayer 
            
poolLayer1=pooling(convLayer1)
poolLayer2=pooling(convLayer2)
poolLayer3=pooling(convLayer3)

one=sn.heatmap(data=poolLayer1,annot=True)
plt.show()
two=sn.heatmap(data=poolLayer2,annot=True)
plt.show()
three=sn.heatmap(data=poolLayer3,annot=True)
plt.show()

