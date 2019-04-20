from PIL import Image
import numpy as np
from libtiff import TIFF
import time
import glob
import os
import PySpin
# import Camera
######## TODO: MAKE SURE TO CHANGE PULLDOWN RESISTOR ON GPIO 12 TO DOWN

open('Data/rawData.txt', 'w').close()
open('Data/processedData.txt', 'w').close()
timeStart = 0
previousTime = 0
ON = 1
previous_file = 'nothing'
stateFile = 'Data/processorState.txt'
file = open(stateFile,"w")
file.write('1')
file.close()



class PortableBiosensorUIProcessingFunctions():
    def __init__(self):
        self.numeratorFunc = self.build_function('Equations/numerator.txt')
        self.denominatorFunc = self.build_function('Equations/denominator.txt')
        self.setAreaOfInterest()
        self.laser1 = 0 # mean value holders
        self.laser2 = 0
        self.laser3 = 0
        self.quantizedTimeStamp = 0
        
    def setAreaOfInterest(self): # call this functionwhenever the AOI params has been changed
        text_file = open("Equations/aoi.txt", "r")
        lines = text_file.read().split('\n')
        text_file.close()
        self.X1 = int(lines[0])
        self.X2 = int(lines[2])
        self.Y1 = int(lines[1])
        self.Y2 = int(lines[3])
        self.numberOfPixels = (self.X2-self.X1)*(self.Y2-self.Y1)
        
    def differenceCalc(self,X,Y): # calculates the differential output of the two input mean based on built diifferential equations
        numerator = self.numeratorFunc(X, Y)
        denominator = self.denominatorFunc(X, Y)
        if denominator == 0:
            return 0
        answer = numerator/denominator
        return answer
        
    def build_function(self,filename): # builds the differential equation from text file
        with open(filename, 'rU') as f:
            eqn = f.read().strip()
            exec("def fcn(X, Y):\n return ({})".format(eqn))
            return locals()['fcn']
            
    def processPic(self,imageName):
        print("processPicCalled: "+ imageName)
        outW = 0
        parsed_name = imageName.split('-')
        laserNumber = int(parsed_name[1])
        timeStamp = float(parsed_name[2])
        while(outW < 500):
            try:
                image_file = TIFF.open(imageName, mode='r')
                outW = 501
            except:
                outW += 1 
        image_gray = image_file.read_image()
        outW = 0
        total = long(0)
        xrange = range(self.X1,self.X2)
        yrange = range(self.Y1,self.Y2)
        for x in xrange:
            for y in yrange:
                numberIn = image_gray[y,x]
                total = total + numberIn
        mean = float(total/(self.numberOfPixels))
        image_file.close()
        if laserNumber == 1:
            self.quantizedTimeStamp = timeStamp
            self.laser1 = mean
            self.updateDataFile(self.quantizedTimeStamp,mean,1,imageName,"Data/rawData.txt")
        if laserNumber == 2:
            self.laser2 = mean
            self.updateDataFile(self.quantizedTimeStamp,mean,2,imageName,"Data/rawData.txt")
        if laserNumber == 3:
            self.laser3 = mean
            self.updateDataFile(self.quantizedTimeStamp,mean,3,imageName,"Data/rawData.txt")
            self.updateDifferenceData(self.quantizedTimeStamp)
            
    def updateDataFile(self, timeStamp,value,laserNumber,imageName,filename):
        with open(filename, "a") as text_file:
            text_file.write(str(timeStamp) +","+str(value)+","+str(laserNumber)+","+imageName+"\n")
            text_file.close()
            
    def updateDifferenceFile(self, timeStamp,value,laserNumber,filename):
        with open(filename, "a") as text_file:
            text_file.write(str(timeStamp) +","+str(value)+","+str(laserNumber)+"\n")
            text_file.close()
            
    def updateDifferenceData(self,timeStamp):
        laser12 = self.differenceCalc(self.laser1,self.laser2)
        laser23 = self.differenceCalc(self.laser2,self.laser3)
        laser31 = self.differenceCalc(self.laser3,self.laser1)
        self.updateDifferenceFile(timeStamp,laser12,12,"Data/processedData.txt")
        self.updateDifferenceFile(timeStamp,laser23,23,"Data/processedData.txt")
        self.updateDifferenceFile(timeStamp,laser31,31,"Data/processedData.txt")
        
    def refreshInfo(self):
        self.numeratorFunc = self.build_function('Equations/numerator.txt')
        self.denominatorFunc = self.build_function('Equations/denominator.txt')
        self.setAreaOfInterest()
        
    def turnOff(self):
        global ON
        ON = 0
        
    def setStartTime(self):
        global startTime
        startTime = time.time()
first=0
app = PortableBiosensorUIProcessingFunctions()
os.system("sudo python Camera.py &")
list_of_files = glob.glob('Biosensor_Images/*')
out = 0
while(out == 0):
    try:
        latest_file = max(list_of_files,key=os.path.getctime)
        out = 1
    except:
        list_of_files = glob.glob('Biosensor_Images/*')
previous_file = latest_file
while (ON != 0):
    list_of_files = glob.glob('Biosensor_Images/*')
    latest_file = max(list_of_files,key=os.path.getctime)
    if(previous_file != latest_file):
        app.processPic(previous_file)
    previous_file = latest_file
    try:
        text_file = open(stateFile, "r")
        lines = text_file.read()
        ON = int(lines[0])
    except:
        ON = 1

try:
    app.processPic(previous_file,timeDiff)
except:
    ON = 0



print('Processor Turned Off')








