import processing as processor
import time

start = time.time()

equation = processor.PortableBiosensorUIProcessingFunctions()
answer = equation.differenceCalc(11100.0,12000.0)
print("answer to difference equation: ")
print(answer)
print("    ")
i = 1
practise1 = "Data/rawData.txt"
filename1 = "Biosensor_Images/830nm_6in.tif"
filename2 = "Biosensor_Images/830nm_12in.tif"
filename3 = "Biosensor_Images/880nm_6in.tif"
filename4 = "Biosensor_Images/880nm_12in.tif"
while i<1201:
    mean1 = equation.processPic(filename1)
    equation.updateDataFile(i,mean1,1,filename1,practise1)
    #print("mean from 830nm_6in.tif: ")
    #print(mean1)
    #print(" ")
    mean2 = equation.processPic(filename2)
    equation.updateDataFile(i,mean2,2,filename2,practise1)
    #print("mean from 830nm_12in.tif: ")
    #print(mean2)
    #print(" ")
    mean3 = equation.processPic(filename3)
    equation.updateDataFile(i,mean3,3,filename3,practise1)
    #print("mean from 880nm_6in.tif: ")
    #print(mean3)
    i = i + 1
    print(i)
end = time.time()
print("done")
print(end-start)
    