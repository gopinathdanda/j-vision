import argparse, cv2, time, imutils, os, math, sys
import numpy as np
from eyetracker import EyeTracker

ap = argparse.ArgumentParser()
ap.add_argument("-f","--faces",help="Path to face classfier (optional)")
ap.add_argument("-e","--eyes",help="Path to eyes classfier (optional)")
ap.add_argument("-i","--images",required=True,help="Path to all image(s)",nargs="+")
args = vars(ap.parse_args())
if args["faces"] is None:
    args["faces"] = "cascades/haarcascade_frontalface_alt.xml"
if args["eyes"] is None:
    args["eyes"] = "cascades/haarcascade_eye.xml"
lowerLim = 300
upperLim = 1500
allLabels = []
label = -1
currName = ""
#faces = []
facesPath = []
currFaces = 0

num_of_images = len(args["images"])

for i,im in enumerate(args["images"]):
    if any(x == os.path.splitext(im)[1][1:] for x in ('jpg','jpeg','png','bmp')):
        # Read image
        image = cv2.imread(im)
        #imagecopy = image.copy()
        imageName = os.path.dirname(im)[7:]
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        
        # Create eyetracker object
        et = EyeTracker(args["faces"],args["eyes"])
        
        # Optimize image size and classify accordingly
        image = imutils.optimize(image,lowerLim,upperLim)
        if image.shape[0]==lowerLim or image.shape[1]==lowerLim:
            allRects = et.track(image,FscaleFactor=1.04,FminNeighbors=3,FminSize=(2,2))
        else:
            allRects = et.track(image)
        
        # Cycle through all faces and eyes
        for (i,rect) in enumerate(allRects):
            if i%3==0:
                (Fx,Fy,Fw,Fh) = rect
                #cv2.rectangle(imagecopy,(Fx,Fy),(Fx+Fw,Fy+Fh),(0,0,255),1)
                face = image[Fy:Fy+Fh,Fx:Fx+Fw]
                e2c = e1c = (0,0)
                #cv2.imshow("Image",imagecopy)
                cv2.imshow("Face"+str(i/3),imutils.resize(face,width=100))
                cv2.waitKey(1)
                continue
            if i%2==0 and i%3!=0:
                #cv2.rectangle(face,(rect[0],rect[1]),(rect[2],rect[3]),(0,0,255),2)
                e2c=((rect[0]+rect[2])/2,(rect[1]+rect[3])/2)
                #print "Red eye: ("+str(e2c[0])+","+str(e2c[1])+")"
            else:
                #cv2.rectangle(face,(rect[0],rect[1]),(rect[2],rect[3]),(0,255,0),2)
                e1c=((rect[0]+rect[2])/2,(rect[1]+rect[3])/2)
                #print "Green eye: ("+str(e1c[0])+","+str(e1c[1])+")"
                continue
            
            # If both eyes not present or angle is more than 10, ignore face
            distEyes = math.sqrt(math.pow((e2c[0]-e1c[0]),2)+math.pow((e2c[1]-e1c[1]),2))*100/face.shape[1]
            angle = abs(math.atan((e1c[1]-e2c[1])/float(e1c[0]-e2c[0])))*180/math.pi
            if e2c==(0,0) or e2c==(0,0) or angle>10:
                continue
            face = imutils.resize(face,width=100)
            #faces.append(face)
            t=time.time()
            folder = "faces/"+imageName
            try:
                os.mkdir(folder)
            except OSError:
                pass
            path = folder+"/"+str(t)+".jpg"
            if currName != imageName:
                label += 1
                if currFaces != 0:
                    print currName+": "+str(currFaces)
                currFaces = 0
                currName = imageName
                allLabels.append(str(label)+";"+currName)
            currFaces += 1
            facesPath.append(path+";"+str(label))
            cv2.imwrite(path,face)
            time.sleep(0.025)
            cv2.imshow("Face Selected",face)
            cv2.waitKey(1)
#print allLabels
fileFolder = "faces/"
with open(fileFolder+"labels.txt","w") as f:
    for l in allLabels:
        f.write(l+"\n")
with open(fileFolder+"imageFiles.txt","w") as f:
    for l in facesPath:
        f.write(l+"\n")
#print "Total number of faces found: %d" % len(faces)