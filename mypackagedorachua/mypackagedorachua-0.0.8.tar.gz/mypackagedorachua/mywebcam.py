import cv2 as cv
import numpy as np
from time import sleep
from datetime import datetime
import sys

class CannotCaptureVideoError(Exception):
    #Raised when there is problem getting video device to capture""
    pass

class MyWebcam:

    def __init__(self,width,height):
        self.width = width
        self.height = height
    

    def startDetection(self, cam, threshold):
        self.cam = cam
        self.cap = cv.VideoCapture(cam,cv.CAP_DSHOW)

        if self.cap is None:
            print("Error getting webcam to video capture")
            raise CannotCaptureVideoError("")

        self.cap.set(3,self.width) # set Width
        self.cap.set(4,self.height) # set Height

        frame1 = None
        frame2 = None

        while frame1 is None:
            frame1 = self.getFrame()
        while frame2 is None:
            frame2 = self.getFrame()

        self.frame1 = frame1
        self.frame2 = frame2

        self.threshold = threshold

        return True
                
    def getFrame(self):        
        ret, frame = self.cap.read()
        return frame

    def saveFrame(self,filename):        
        ret, frame = self.cap.read()
        cv.imwrite(filename,frame)
        return frame

        
    def senseMotion(self):        
        
        diff = cv.absdiff(self.frame1, self.frame2)

        diff_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(diff_gray, (5, 5), 0)
        _, thresh = cv.threshold(blur, self.threshold, 255, cv.THRESH_BINARY)
        dilated = cv.dilate(thresh, None, iterations=3)
        contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        self.frame1 = self.frame2
        self.frame2 = self.getFrame()
                
        return len(contours)>0

        
    def stopDetection(self):
        self.cap.release()
        cv.destroyAllWindows() 
        

if __name__ == "__main__":

    try:

        cv.__version__

        mywebcam = MyWebcam(640,480)
        
        mywebcam.startDetection(0,200)

        while True:
            
            dts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            motiondetected = mywebcam.senseMotion()        

            if motiondetected == True:
                print("Motion detected")
                mywebcam.saveFrame(dts.replace(":",".") + ".jpg")
            
            if cv.waitKey(50) == 27:
                mywebcam.stopDetection()
                break

            sleep(1)
            
    except CannotCaptureVideoError:
        print("Error initializing video device")
        sys.exit()

    except KeyboardInterrupt:
        print('Interrupted')
        mywebcam.stopDetection()
        sys.exit()

    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

