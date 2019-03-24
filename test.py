import processing as processor

equation = processor.PortableBiosensorUIProcessingFunctions()
answer = equation.differenceCalc(1.0,1.0)
i = 1
practise1 = "Data/rawData.txt"
filename1 = "Biosensor_Images/830nm_6in.tif"
filename2 = "Biosensor_Images/830nm_12in.tif"
filename3 = "Biosensor_Images/880nm_6in.tif"
filename4 = "Biosensor_Images/880nm_12in.tif"
while i<100:
    mean1 = equation.processPic(filename1)
    equation.updateDataFile(i,mean1,1,filename1,practise1)
    mean2 = equation.processPic(filename2)
    equation.updateDataFile(i,mean2,2,filename2,practise1)
    mean3 = equation.processPic(filename3)
    equation.updateDataFile(i,mean3,3,filename3,practise1)
    i = i + 1