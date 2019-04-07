import os
# run this on new machines to create the file structure needed for main.py and processing.py


os.system("sudo mkdir Biosensor_Images")
os.system("sudo mkdir Data")
os.system("sudo touch processedData.txt")
os.system("sudo touch rawData.txt")
os.system("sudo mkdir Equations")
os.system("sudo touch aoi.txt")
os.system("sudo touch denominator.txt")
os.system("sudo touch numerator.txt")