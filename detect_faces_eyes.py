import argparse, cv2, time, imutils, os, cmath, math, sys
import numpy as np
from eyetracker import EyeTracker

ap = argparse.ArgumentParser()
ap.add_argument("-f","--faces",help="Path to face classfier (optional)")
ap.add_argument("-e","--eyes",help="Path to eyes classfier (optional)")
ap.add_argument("-i","--images",required=True,help="Path to all image(s)",nargs="+")
args = vars(ap.parse_args())
lowerLim = 300
upperLim = 1500
allLabels = []
label = -1
currName = ""
faces = []
facesPath = []

# Progress bar
toolbar_width = 40
counter = 0
sys.stdout.write("#")
sys.stdout.flush()
num_of_images = len(args["images"])

for i,im in enumerate(args["images"]):
    if i*toolbar_width/num_of_images>counter:
        counter=counter+1
        sys.stdout.write("#")
    percent = ((i+1)*100/float(num_of_images))
    sys.stdout.write(" %0.2f%%" % percent)
    sys.stdout.flush()
    if percent<10:
        sys.stdout.write("\b"*6)
    else:
        sys.stdout.write("\b"*7)
    if any(x == os.path.splitext(im)[1][1:] for x in ('jpg','jpeg','gif','png','bmp')):
        # Read image
        image = cv2.imread(im)
        imageName = os.path.dirname(im)[7:]
        # Grayscale image
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        # Create facedetector object
        if args["faces"] is None:
            args["faces"] = "cascades/haarcascade_frontalface_alt.xml"
        if args["eyes"] is None:
            args["eyes"] = "cascades/haarcascade_eye.xml"
        et = EyeTracker(args["faces"],args["eyes"])
        # Optimize image size
        image = imutils.optimize(image,lowerLim,upperLim)
        # If size is 300 use custom parameter values, else use default (have to make it dynamic)
        if image.shape[0]==lowerLim or image.shape[1]==lowerLim:
            allRects = et.track(image,FscaleFactor=1.04,FminNeighbors=3,FminSize=(2,2))
        else:
            allRects = et.track(image)
        for (i,rect) in enumerate(allRects):
            if i%3==0:
                (Fx,Fy,Fw,Fh) = rect
                #cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),1)
                face = image[Fy:Fy+Fh,Fx:Fx+Fw]
                e2c=e1c=(0,0)
                #print "Face"+str(i/3)+": ("+str(rect[0])+","+str(rect[1])+")"
                cv2.imshow("Face"+str(i/3),imutils.resize(face,width=100))
                cv2.waitKey(1000)
                continue
            if i%2==0 and i%3!=0:
                #cv2.rectangle(face,(rect[0],rect[1]),(rect[2],rect[3]),(0,0,255),2)
                e2c=((rect[0]+rect[2])/2,(rect[1]+rect[3])/2)
                #print "Red eye: ("+str(rect[0])+","+str(rect[1])+")"
            else:
                #cv2.rectangle(face,(rect[0],rect[1]),(rect[2],rect[3]),(0,255,0),2)
                e1c=((rect[0]+rect[2])/2,(rect[1]+rect[3])/2)
                #print "Green eye: ("+str(rect[0])+","+str(rect[1])+")"
                continue
            angle = abs(cmath.atan((e1c[1]-e2c[1])/float(e1c[0]-e2c[0])))*180/math.pi
            # If both eyes not present or angle is more than 10, ignore face
            if e2c==(0,0) or e2c==(0,0) or angle>10:
                continue
            face = imutils.resize(face,width=100)
            faces.append(face)
            t=time.time()
            folder = "faces/"+imageName
            try:
                os.mkdir(folder)
            except OSError:
                pass
            path = folder+"/"+str(t)+".jpg"
            if currName != imageName:
                label += 1
                currName = imageName
                allLabels.append(str(label)+";"+currName)
            facesPath.append(path+";"+str(label))
            cv2.imwrite(path,face)
            time.sleep(0.025)
            cv2.imshow("Face Selected",face)
            cv2.waitKey(1000)
        #cv2.imshow("Original",gray)
        #cv2.waitKey(1000)
#print allLabels[:]
sys.stdout.write("\n")
fileFolder = "faces/"
with open(fileFolder+"labels.txt","w") as f:
    for l in allLabels:
        f.write(l+"\n")
with open(fileFolder+"imageFiles.txt","w") as f:
    for l in facesPath:
        f.write(l+"\n")
print "Total number of faces found: %d" % len(faces)