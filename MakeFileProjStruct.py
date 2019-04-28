import os
# run this on new machines to create the file structure needed for main.py and processing.py

os.system("sudo touch Data/processedData.txt")
os.system("sudo touch Data/rawData.txt")
os.system("sudo touch Equations/aoi.txt")
os.system("sudo touch Equations/denominator.txt")
os.system("sudo touch Equations/numerator.txt")

os.system("sudo touch Data/processorState.txt")
file = open('Data/processorState.txt',"w")
file.write('0')
file.close()