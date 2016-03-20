import numpy as np
import argparse
import imutils
import cv2

global gray,rX,rY

def updateRX(val):
    global rX
    rX = val-midX
    cv2.imshow("Gray",imutils.translate(gray,rX,rY))
def updateRY(val):
    global rY
    rY = val-midY
    cv2.imshow("Gray",imutils.translate(gray,rX,rY))
def scaleC(val):
    global gray
    empty = np.zeros(gray.shape[:2],dtype="uint8")
    if val == 0:
        scaled = imutils.scale(gray,1/float(10))
    else:
        scaled = imutils.scale(gray,val/float(10))
    if scaled.shape[0] > empty.shape[0] or scaled.shape[1] > empty.shape[1]:
        empty = scaled[0:empty.shape[0],0:empty.shape[1]]
    else:
        empty[0:scaled.shape[0],0:scaled.shape[1]] = scaled
    cv2.imshow("Gray",empty)
    
ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="Path to image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
(midY,midX) = image.shape[:2]
rX = rY = 0
scale = 1
gray2 = imutils.translate(gray,rX,rY)
cv2.imshow("Gray",imutils.scale(gray,scale))

cv2.imshow("Image",image)
cv2.imshow("Gray",gray)
cv2.createTrackbar("Translate-x","Gray",midX-rX,image.shape[1]*2,updateRX)
cv2.createTrackbar("Translate-y","Gray",midY-rY,image.shape[0]*2,updateRY)
cv2.createTrackbar("Scale","Gray",10,20,scaleC)
cv2.waitKey(0)
