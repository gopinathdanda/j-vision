import numpy as np
import scipy.special as sc

# neural network class definition
class NN:
    
    # initialize
    def __init__(self,inputnodes,hiddennodes,outputnodes,learningrate):
        # set the number nodes in each input, hidden and output layer
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes
        
        # set learning rate
        self.lr = learningrate
        
        # link weight matrices
        self.wih = np.random.normal(0.0,pow(self.inodes,-0.5),(self.hnodes,self.inodes))
        self.who = np.random.normal(0.0,pow(self.hnodes,-0.5),(self.onodes,self.hnodes))
        
        # activation function
        self.activation_function = lambda x: sc.expit(x)
        
        pass
    
    # train
    def train(self,inputs_list,targets_list):
        # convert lists to 2d arrays and transpose them
        inputs = np.array(inputs_list,ndmin=2).T
        targets = np.array(targets_list,ndmin=2).T
        
        # hidden layer calculation
        hidden_inputs = np.dot(self.wih,inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # final layer calculations
        final_inputs = np.dot(self.who,hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        
        # output errors
        output_errors = targets-final_outputs
        # hidden errors
        hidden_errors = np.dot(self.who.T,output_errors)
        # update hidden_output weights
        self.who += self.lr*np.dot((output_errors*final_outputs*(1.0-final_outputs)),np.transpose(hidden_outputs))
        # update input_hidden weights
        self.wih += self.lr*np.dot((hidden_errors*hidden_outputs*(1.0-hidden_outputs)),np.transpose(inputs))
        
        pass
        
    # query
    def query(self,inputs_list):
        # convert inputs_list to 2d array and transpose it
        inputs = np.array(inputs_list,ndmin=2).T
        
        # hidden inputs
        hidden_inputs = np.dot(self.wih,inputs)
        
        # hidden outputs
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # final output layer inputs
        final_inputs = np.dot(self.who,hidden_outputs)
        
        # final outputs
        final_outputs = self.activation_function(final_inputs)
        
        return final_outputs

    def weights(self):
        return [self.wih,self.who]