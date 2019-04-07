
import time
import os
import glob
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

def writeToTextFile(nameOfFile,textToBeSaved): # writes over the current text file with the input information
    file = open(nameOfFile,"w")
    file.write(textToBeSaved)
    file.close()
i = 0
while i<5:
    i += 1
    GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(12,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    val1 = GPIO.input(11)
    val2 = GPIO.input(12)
    laserState = 1*val1+2*val2
    #print(laserState)
    time.sleep(1.5)
    GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(12,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    val1 = GPIO.input(11)
    val2 = GPIO.input(12)
    laserState = 1*val1+2*val2
    #print(laserState)
    time.sleep(1.5)
    GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(12,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    val1 = GPIO.input(11)
    val2 = GPIO.input(12)
    laserState = 1*val1+2*val2
    #print(laserState)
    time.sleep(1.5)
    #print('end')

writeToTextFile('Data/processorState.txt','0')
os.system("sudo mkdir /media/pi/EXTSTORAGE/Portable_Biosensor_Data")
os.system("sudo cp -r Biosensor_Images /media/pi/EXTSTORAGE/Portable_Biosensor_Data/.")
os.system("sudo rm Biosensor_Images/*.tiff")
os.system("sudo cp -r Data /media/pi/EXTSTORAGE/Portable_Biosensor_Data/.")
os.system("sudo rm Data/*.txt")