#create a perceptron
#forward prop
#backprop
#update weights
import random
class Perceptron:
    def __init__(self, learning_rate=0.1, n_iterations=1000):
        self.learning_rate=0.1
        self.n_iterations=n_iterations
        self.weights=None
        self.bias=None

    def activation_function(self, net_input):
        #if x >= 0: 1, else 0
        #STEP ACTIVATION
        for row in range(len(net_input)):
            for col in range(len(net_input[0])):
                if net_input[row][col]>=0:
                    net_input[row][col]=1
                else:
                    net_input[row][col]=0

    def fit(self, features, targets):
        pass
        n_examples, n_features = n_features.shape
        #get shape of features, itll be useful
        #create random weights(-.5 to .5) and random biases (also -.5 to .5)
        self.weights=[]
        self.bias=[]
        for row in range(len(n_examples)):
            w=[]
            b=[]
            for col in range(len(n_features)):
                w.append(random.uniform(-0.5,0.5))
                b.append(random.uniform(-0.5,0.5))
            self.weights.append(w)
            self.bias.append(b)
        for n in range(self.n_iterations):
            for example_index, example_feature in enumerate(features): #these are the rows of features
                #for n interations: dot and add bias matrix, activaion on that, then update weights
                net_input=[]
                for row in range(len(example_feature)):
                    l=[]
                    for col in range(len(example_features[row])):
                        #weight[i]*input[i]+bias[i]
                        l.append((example_features[row][col]*self.weights[row][col])+self.bias[row][col]) 
                    net_input.append(l)
                #apply activation
                y_pred=self.activation_function(net_input)
                self.update_weights(example_features, targets[example_index], y_pred)

    def update_weights(self, example_features, y_actual, y_predict):
        #get error
        error=[]
        for row in range(len(y_actual)):
            l=[]
            for col in range(len(y_actual[row])):
                l.append(y_actual[row][col] - y_predict[row][col])
            error.append(l)
        #weight correction = multiply error by learning rate
        weight_correction=[]
        for row in range(len(error)):
            l=[]
            for col in range(len(error[row])):
                l.append(error[row][col] * self.learning_rate)
            weight_correction.append(l)
        #update weight and bias w respect to weight correction
        #self.weights = self.weights + weight_correction * example_features
        for row in range(len(self.weights)):
            for col in range(len(self.weights[row])):
                    self.weights[row][col]=self.weights[row][col]+weight_correction[row][col]*example_features[row][col]

    def predict(self, features):
        net_input=[]
        for row in range(len(features)):
            l=[]
            for col in range(len(features[row])):
                l.append((features[row][col]*self.weights[row][col])+self.bias[row][col])
        final_prediction=self.activation_function(net_input)
        return final_prediction
        #final dot, final activation, return

#when adding or doing dot product, do manually, dont use numpy

class Preprocessing:
    def __init__(self):
        pass
    def train_test_split(self, test_size=0.2):
        pass

