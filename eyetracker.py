import cv2

class EyeTracker:
    def __init__(self, faceCascadePath, eyeCascadePath):
        self.faceCascade = cv2.CascadeClassifier(faceCascadePath)
        self.eyeCascade = cv2.CascadeClassifier(eyeCascadePath)
        
    def track(self,image,FscaleFactor=1.1,FminNeighbors=5,FminSize=(30,30),EscaleFactor=1.1,EminNeighbors=10,EminSize=(20,20)):
        faceRects = self.faceCascade.detectMultiScale(image,scaleFactor=FscaleFactor,minNeighbors=FminNeighbors,minSize=FminSize,flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
        rects = []
        for (fX,fY,fW,fH) in faceRects:
            faceROI = image[fY:fY+fH, fX:fX+fW]
            rects.append((fX,fY,fW,fH))
            
            eyeRects = self.eyeCascade.detectMultiScale(faceROI,scaleFactor=EscaleFactor,minNeighbors=EminNeighbors,minSize=EminSize,flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
            
            for (eX,eY,eW,eH) in eyeRects:
                rects.append((eX,eY,eX+eW,eY+eH))
        return rects