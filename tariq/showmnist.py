import numpy as np
import matplotlib.pyplot as plt
import nn

input_nodes = 28*28 # size of image
hidden_nodes = 200
output_nodes = 10
learning_rate = 0.1

n = nn.NN(input_nodes,hidden_nodes,output_nodes,learning_rate)

# training the neural net

epochs = 5

tr_file = open('mnist_train.csv','r')
tr_list = tr_file.readlines()
tr_file.close()

for e in range(epochs):
    for record in tr_list:
        all_values = record.split(',')
        inputs = (np.asfarray(all_values[1:])/255.0*0.99) + 0.01 # scaling input to be between 0.01-1.00
        #print(inputs)
        #image_array = np.asfarray(all_values[1:]).reshape((28,28))
        #plt.imshow(image_array,cmap='Greys',interpolation='None')
        #plt.show()    
    
        targets = np.zeros(output_nodes)+0.01 # scaling output to be between 0.01-0.99
        targets[int(all_values[0])] = 0.99
        #print(targets)
        n.train(inputs,targets)
        pass
    pass

# testng the neural net

tst_file = open('mnist_test.csv','r')
tst_list = tst_file.readlines()
tst_file.close()

'''
all_values = tst_list[0].split(',')
print(all_values[0])
image_array = np.asfarray(all_values[1:]).reshape((28,28))
plt.imshow(image_array,cmap='Greys',interpolation='None')
plt.show()
print(n.query((np.asfarray(all_values[1:])/255.0*0.99) + 0.01))
'''

scorecard = []

for record in tst_list:
    all_values = record.split(',')
    inputs = (np.asfarray(all_values[1:])/255.0*0.99) + 0.01 # scaling input to be between 0.01-1.00
    correct_label = int(all_values[0])
    #print(correct_label,"correct label")
    
    outputs = n.query(inputs)
    
    label = np.argmax(outputs)
    #print(label,"nn answer")
    
    if(correct_label == label):
        scorecard.append(1)
    else:
        scorecard.append(0)
        #image_array = np.asfarray(all_values[1:]).reshape((28,28))
        #plt.imshow(image_array,cmap='Greys',interpolation='None')
        #plt.show()
        pass

    pass

scorecard_array = np.asarray(scorecard)
print("performance = ",scorecard_array.sum()/scorecard_array.size)
