# simulates the connection between the raspberry pi and arduino for testing purposes
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

while i<8:
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
    print("ITERATION: ")
    print(i)
    #print('end')

writeToTextFile('Data/processorState.txt','0')
GPIO.cleanup()














