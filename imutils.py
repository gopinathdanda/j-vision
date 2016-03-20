import numpy as np
import cv2

def resize(image,width=None,height=None,interpolation=cv2.INTER_AREA):
    (h,w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        ratio = height/float(h)
        width = int(ratio*w)
    elif height is None:
        ratio = width/float(w)
        height = int(ratio*h)
    dim = (width,height)
    return cv2.resize(image,dim,interpolation=interpolation)

def scale(image,ratio):
    return resize(image,int(image.shape[1]*ratio),int(image.shape[0]*ratio))

def translate(image,x,y):
    (h,w) = image.shape[:2]
    rotX = [1,0,x]
    rotY = [0,1,y]
    rot = np.float32([rotX,rotY])
    return cv2.warpAffine(image,rot,(w,h))
    
def rotate(image,degree,center=None,scale=1.0):
    (h,w) = image.shape[:2]
    if center is None:
        center = (w/2,h/2)
    return cv2.warpAffine(image,cv2.getRotationMatrix2D(center,degree,scale),(w,h))
    