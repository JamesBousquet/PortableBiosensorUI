import RPi.GPIO as GPIO
from PIL import Image
import numpy as np
from libtiff import TIFF

######## TODO: MAKE SURE TO CHANGE PULLDOWN RESISTOR ON GPIO 12 TO DOWN

open('Data/rawData.txt', 'w').close()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12,GPIO.IN, pull_up_down=GPIO.PUD_UP) # ***** CHANGE TO DOWN WHEN DONE TESTING

class PortableBiosensorUIProcessingFunctions():
    def __init__(self):
        self.numeratorFunc = self.build_function('Equations/numerator.txt')
        self.denominatorFunc = self.build_function('Equations/denominator.txt')
        self.setAreaOfInterest()
        self.laserState = 0
        
    def setAreaOfInterest(self): # call this functionwhenever the AOI params has been changed
        text_file = open("Equations/aoi.txt", "r")
        lines = text_file.read().split('\n')
        print lines
        print len(lines)
        text_file.close()
        self.X1 = int(lines[0])
        self.X2 = int(lines[2])
        self.Y1 = int(lines[1])
        self.Y2 = int(lines[3])
        print(self.X1)
        print(self.X2)
        print(self.Y1)
        print(self.Y2)
        self.numberOfPixels = (self.X2-self.X1)*(self.Y2-self.Y1)
    def differenceCalc(self,X,Y): # calculates the differential output of the two input mean based on built diifferential equations
        numerator = self.numeratorFunc(X, Y)
        print("numerator:")
        print(numerator)
        denominator = self.denominatorFunc(X, Y)
        print("denominator:")
        print(denominator)
        answer = numerator/denominator
        print("answer: ")
        print(answer)
        return answer
        
    def build_function(self,filename): # builds the differential equation in two seperate parts
        with open(filename, 'rU') as f:
            eqn = f.read().strip()
            exec("def fcn(X, Y):\n return ({})".format(eqn))
            return locals()['fcn']
    def processPic(self,imageName):
        image_file = TIFF.open(imageName, mode='r')
        image_gray = image_file.read_image()
        print(" ")
        total = long(0)
        for x in range(self.X1,self.X2):
            for y in range(self.Y1,self.Y2):
                numberIn = long(image_gray[y,x])
                total = total + numberIn
        print("mean: ")
        mean = float(total/self.numberOfPixels)
        image_file.close()
        print(mean)
        return mean
        
    def updateLaserState(self):
        val1 = GPIO.input(11)
        val2 = GPIO.input(12)
        self.laserState = 1*val1+2*val2
    def getLaserState(self):
        self.updateLaserState()
        return self.laserState
    def updateDataFile(self, timeStamp,value,laserNumber,imageName,filename):
        with open(filename, "a") as text_file:
            
            text_file.write(str(timeStamp) +","+str(value)+","+str(laserNumber)+","+imageName+"\n")
            text_file.close()
            











