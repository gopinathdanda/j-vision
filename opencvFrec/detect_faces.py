import argparse, cv2, time, imutils, os
import numpy as np
from facedetector import FaceDetector

ap = argparse.ArgumentParser()
ap.add_argument("-f","--faces",help="Path to face classfier (optional)")
ap.add_argument("-i","--images",required=True,help="Path to all image(s)",nargs="+")
args = vars(ap.parse_args())
faces=[]
lowerLim = 300
upperLim = 1500

for im in args["images"]:
    if any(x == os.path.splitext(im)[1][1:] for x in ('jpg','jpeg','gif','png','bmp')):
        # Read image
        image = cv2.imread(im)
        # Grayscale image
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        # Create facedetector object
        if args["faces"] is None:
            fd = FaceDetector("cascades/haarcascade_frontalface_alt.xml")
        else:
            fd = FaceDetector(args["faces"])
        # Optimize image size
        image = imutils.optimize(image,lowerLim,upperLim)
        # If size is 300 use custom parameter values, else use default (have to make it dynamic)
        if image.shape[0]==lowerLim or image.shape[1]==lowerLim:
            faceRects = fd.detect(image,scaleFactor=1.04,minNeighbors=3,minSize=(2,2))
        else:
            faceRects = fd.detect(image)
        for (i,rect) in enumerate(faceRects):
            (x,y,w,h) = rect
            #cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),1)
            face = imutils.resize(image[y:y+h,x:x+w],width=100)
            faces.append(face)
            t=time.time()
            folder = "faces/"+os.path.dirname(im)[7:]
            try:
                os.mkdir(folder)
            except OSError:
                pass
            cv2.imwrite(folder+"/"+str(t)+".jpg",face)
            time.sleep(0.025)
            cv2.imshow("Face",face)
            cv2.waitKey(1000)
        #cv2.imshow("Original",gray)
        #cv2.waitKey(1000)
print "Number of faces found: %d" % len(faces)