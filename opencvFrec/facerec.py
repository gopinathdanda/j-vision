import numpy as np
import cv2, argparse, imutils, random

def normalize(X, low, high, dtype=None):
    """Normalizes a given array in X to a value between low and high."""
    X = np.asarray(X)
    minX, maxX = np.min(X), np.max(X)
    # normalize to [0...1].
    X = X - float(minX)
    X = X / float((maxX - minX))
    # scale to [low...high].
    X = X * (high-low)
    X = X + low
    if dtype is None:
        return np.asarray(X)
    return np.asarray(X, dtype=dtype)

def randomize(a):
    b = []
    for i in range(len(a)):
        element = random.choice(a)
        a.remove(element)
        b.append(element)
    return b

def trainAndTest(train=80,imagesList="faces/imageFiles.txt",facesList="faces/labels.txt"):
    images = imagesList
    labels = facesList

    labels_list = []
    main_list = []
    X_train,Y_train = [],[]
    X_test,Y_test = [],[]
    X_test_im = []

    for line in open(labels,'r'):
        v = line.rstrip('\n').split(';')
        labels_list.append(v[1])

    for line in open(images,'r'):
        main_list.append(line.rstrip('\n'))
    random_list = randomize(main_list)
    index = int(train*len(random_list)/100)-1

    for k,v in enumerate(random_list):
        (i,l) = v.split(';')
        im = cv2.imread(i,cv2.IMREAD_GRAYSCALE)
        im_resized = imutils.resize(im,width=100,height=100)
        if k <= index:
            X_train.append(np.asarray(im_resized, dtype=np.uint8))
            Y_train.append(l)
        else:
            X_test_im.append(i)
            X_test.append(np.asarray(im_resized, dtype=np.uint8))
            Y_test.append(l)

    Y_train = np.asarray(Y_train, dtype=np.int32)
    Y_test = np.asarray(Y_test, dtype=np.int32)
    model = cv2.createLBPHFaceRecognizer()
    model.train(np.asarray(X_train),np.asarray(Y_train))

    #test = random.randint(0,len(Y_test))
    #test_im = X_test[test]
    #test_image = cv2.imread(X_test_im[test])
    #print "Actual: %s" % (labels_list[Y_test[test]])

    correct = 0
    total_test = len(Y_test)

    for i,test_im in enumerate(X_test):
        [p_l, p_c] = model.predict(np.asarray(test_im))
        a_l = Y_test[i]
        if a_l == p_l:
            correct += 1
        #print "Predicted value: %s (confidence level = %0.2f)" % (labels_list[int(p_l)], p_c)

    return (correct/float(total_test))

acc = 0
tot = 25
trainList = [50,60]
accList = []

for v in trainList:
    for count in range(0,tot):
        accuracy = trainAndTest(train=v)
        acc += accuracy
        avg = acc/float(count+1)
        #print "%d:: %d samples have %0.2f accuracy" % (count,v,accuracy)
        print "%d:: avg: %0.2f" %(count,avg)
    acc = acc/float(tot)
    accList.append(acc)
    acc = 0
print "---------------------------"
for i,v in enumerate(trainList):
    print "%d samples: %0.2f" % (v,accList[i])
#mean = model.getMat("mean")
#eigenvectors = model.getMat("eigenvectors")
#mean_norm = normalize(mean, 0, 255, dtype=np.uint8)
#mean_resized = mean_norm.reshape(test_im.shape)
#cv2.imshow("Actual",test_image)
#cv2.waitKey(0)
#print model.getParams()