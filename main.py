''' INFORMATION#
Using Python 2
Must start program from sudo user to write successfully
to run navigate to SampleUI file in terminal and launch with "sudo python main.py &"
Whenever adding a new page, must add it to container class

NEED numpy 1.16 for camera to work


TODO
add videos
'''
import os
os.system("sudo sh -c 'echo 1000 > /sys/module/usbcore/parameters/usbfs_memory_mb'")
os.system("sudo python Alignment.py &")
import matplotlib
import glob
from libtiff import TIFF
import RPi.GPIO as GPIO
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import time
import Tkinter as tk
import tkFont
import ttk
from ttk import *
import tkMessageBox
from Tkinter import *
from PIL import Image, ImageTk
GPIO.setmode(GPIO.BOARD)





originalImageWidth = 1288
originalImageHeight = 964
BORDERWIDTH = 0.0
BLUE_COLOR = '#3f88bf'
WHITE_COLOR = '#1D69A4' # Red = 29  Green = 105  Blue = 164
TEXT_COLOR = '#ffffff'
BUTTON_COLOR = '#1D69A4'
TITLE_FONT = ("Arial", 36)
LARGE2_FONT = ("Arial", 20)
LARGE_FONT = ("Arial", 16)
MEDIUM_FONT = ("Arial", 12)
SMALL_FONT = ("Arial", 8)
style.use("ggplot")
iconSize = (260,260)
buttonSizeLarge = (300,51)
buttonSize = (300,51)#buttonSize = (200,35)
buttonSizeSmall = (170,35)
SMALLBUTTON_FONT = MEDIUM_FONT

YMAX = 1


#mostRecentPhotoName = 'Biosensor_Images/880nm_12in.tif'
#mostRecentPhotoFigure = Figure(figsize=(5,5), dpi=100)

f = Figure(figsize=(5,5), dpi=100)
rawPlot = f.add_subplot(121) # 121 = 1x2 figure plot number 1
processedPlot = f.add_subplot(122) # 121 = 1x2 figure plot number 2
'''
rawPlot.xlabel('Seconds')
rawPlot.ylabel('Raw Values')
processedPlot.xlabel('Seconds')
processedPlot.ylabel('Difference Equation Values')
'''

# animation function for displaying graphs
def animate(i): 
    if app.PAUSE == False:
        global YMAX
        pullData = []
        pullData.append(open("Data/rawData.txt","r").read())
        rawPlot.clear()
        for eachFile in pullData:
            dataList = eachFile.split('\n')
            xList1 = []
            yList1 = []
            xList2 = []
            yList2 = []
            xList3 = []
            yList3 = []
            for eachLine in dataList:
                if len(eachLine) > 1:
                    x, y,laserNumberTxt,filename = eachLine.split(',')
                    laserNumber = int(laserNumberTxt)
                    if(laserNumber==1):
                        xList1.append(float(x))
                        yList1.append(float(y))
                    if(laserNumber==2):
                        xList2.append(float(x))
                        yList2.append(float(y))
                    if(laserNumber==3):   
                        xList3.append(float(x))
                        yList3.append(float(y))
        rawPlot.scatter(xList1, yList1, color = 'r',label = 'Laser 1')
        rawPlot.scatter(xList2, yList2, color = '#ffff05',label = 'Laser 2')
        rawPlot.scatter(xList3, yList3, color = 'b',label = 'Laser 3')
        pullDataProcessed = []
        pullDataProcessed.append(open("Data/processedData.txt","r").read())
        i = 1
        processedPlot.clear()
        ymax = .1
        for eachFile in pullDataProcessed:
            dataList = eachFile.split('\n')
            xList12 = []
            yList12 = []
            xList23 = []
            yList23 = []
            xList31 = []
            yList31 = []
            for eachLine in dataList:
                if len(eachLine) > 1:
                    x, y,laserNumberTxt = eachLine.split(',')
                    laserNumber = int(laserNumberTxt)
                    if (float(y) > YMAX):
                        YMAX = float(y)
                    if(laserNumber==12):
                        xList12.append(float(x))
                        yList12.append(float(y))
                    if(laserNumber==23):
                        xList23.append(float(x))
                        yList23.append(float(y))  
                    if(laserNumber==31):
                        xList31.append(float(x))
                        yList31.append(float(y))
        processedPlot.scatter(xList12, yList12, color = '#ffa500',label = 'Lasers 1 and 2')
        processedPlot.scatter(xList23, yList23, color = 'g',label = 'Lasers 2 and 3')
        processedPlot.scatter(xList31, yList31, color = 'm',label = 'Lasers 3 and 1')
        try:
            xmax = int(xList1[-1]+5)
            ymax = 1.2*float(YMAX)
        except:
            xmax = 10
        rawPlot.set_ylim([0,66000])
        rawPlot.set_xlim([0,xmax])
        processedPlot.set_ylim([0,ymax])
        processedPlot.set_xlim([0,xmax])
        rawPlot.set_title('Raw Data')
        processedPlot.set_title('Difference Equation Data')
        #rawPlot.xlabel('Seconds')
        #rawPlot.ylabel('Raw Values')
        #processedPlot.xlabel('Seconds')
        #processedPlot.ylabel('Difference Equation Values')
        rawPlot.legend(bbox_to_anchor=(0,0,2,.102), loc=3, ncol=2, borderaxespad=1)
        processedPlot.legend(bbox_to_anchor=(0,0,2,.102), loc=3, ncol=2, borderaxespad=1)
class PortableBiosensorUI(tk.Tk):
    # Container Class, add a new page here after the class is created
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args, **kwargs)
        self.PAUSE = True
        img = Image.open('UIPictures/blue_button3.png')
        resizedImg=img.resize(buttonSize, Image.ANTIALIAS)
        resizedSmallImg = img.resize(buttonSizeSmall, Image.ANTIALIAS)
        self.buttonBackground = ImageTk.PhotoImage(resizedImg)
        self.buttonBackgroundSmall = ImageTk.PhotoImage(resizedSmallImg)
	
        container = tk.Frame(self)
        self.geometry('1250x700')
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = { }
        for F in (StartPage, HelpPage, TestPrepPage, GUIPage, PictureDisplayPage, DifferenceEquationEditorPage, AreaOfInterestPage,AlignmentCameraPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        menu = tk.Menu(self,bg = "blue",fg=TEXT_COLOR,font = MEDIUM_FONT)
        self.config(menu=menu)
	self.currentFrame = StartPage
        self.show_frame(StartPage)
        menu.add_command(label="Start Page", command = self.backToStartPage)
	menu.add_command(label="Return", command = self.showPreviousPage)
        self.show_frame(StartPage)
    def show_frame(self,cont):
	self.previousFrame = self.currentFrame
        frame = self.frames[cont]
        frame.tkraise() # raises the frame to the front
	self.currentFrame = cont
        
    def backToStartPage(self):
        answer = tkMessageBox.askquestion('Return to Start Page', message = 'Are you sure you want to return to start page? Any tests will end if continued.', icon = 'warning')
        if answer == 'yes':
            app.PAUSE = True
            turnOffProcessor()
            turnOffCamera()
            self.show_frame(StartPage)
            transferDataToStorage()
    def showPreviousPage(self):
	self.show_frame(self.previousFrame)

# Pages
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent,bg=WHITE_COLOR)
        label = tk.Label(self,text="Welcome to the Portable Biosensor UI!", font=TITLE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        label.pack(pady=10, padx=10)
        
        self.subframe = tk.Frame(self,bg=WHITE_COLOR)
        self.subframe.pack(side="top",padx=250,pady = 30)
        #help_button = tk.Button(self.subframe, highlightthickness = 0, image=controller.buttonBackground,text="Need Help?",borderwidth=BORDERWIDTH,compound=CENTER,command=lambda: controller.show_frame(HelpPage),background=BUTTON_COLOR,foreground=TEXT_COLOR)
        #help_button.pack(side=tk.LEFT,padx=15)
        testPrep_button = tk.Button(self.subframe, font = LARGE2_FONT, highlightthickness = 0, image=controller.buttonBackground,compound=CENTER,text="Start Test Preperation",command=lambda: controller.show_frame(TestPrepPage),background=BUTTON_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        testPrep_button.pack(side=tk.LEFT,padx=15)
        
        load = Image.open('UIPictures/teamlogo.png')
        render = ImageTk.PhotoImage(load)
        
        logo = Label(self,image=render)
        logo.image = render
        logo.pack(side=tk.TOP)
        
        
class HelpPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent,bg=WHITE_COLOR)
        label = tk.Label(self, text="Help Page", font=TITLE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        label.pack(pady=10, padx=10)
        

class TestPrepPage(tk.Frame):
    def __init__(self,parent,controller):
        self.controller = controller
        tk.Frame.__init__(self, parent,bg=WHITE_COLOR)
        self.buttonFrame = Frame(self,bg=WHITE_COLOR)
        label = tk.Label(self, text="Test Preparation Menu", font=TITLE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        label.pack(pady=20, padx=10)
        
        #instructionsLabel = tk.Label(self,text="Select desired option and hit Start Test when ready", font=LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        #instructionsLabel.pack(pady=10)
        
        # making the icons as buttons
        loadCameraIcon = Image.open('UIPictures/camera_icon.png')
        resizedCameraIcon=loadCameraIcon.resize(iconSize, Image.ANTIALIAS)
        renderCameraIcon = ImageTk.PhotoImage(resizedCameraIcon)
        cameraIconPic = Label(self.buttonFrame,image=renderCameraIcon)
        cameraIconPic.image = renderCameraIcon
        cameraIconPic.grid(row=0,column=0,padx=15,pady=5)
        cameraIconPic.bind("<Button-1>", self.cameraEvent)
        
        loadEquationIcon = Image.open('UIPictures/equation_icon.png')
        resizedEquationIcon=loadEquationIcon.resize(iconSize, Image.ANTIALIAS)
        renderEquationIcon = ImageTk.PhotoImage(resizedEquationIcon)
        equationIconPic = Label(self.buttonFrame,image=renderEquationIcon)
        equationIconPic.image = renderEquationIcon
        equationIconPic.grid(row=0,column=1,padx=15,pady=5)
        equationIconPic.bind("<Button-1>", self.equationEvent)
        
        loadAOIIcon = Image.open('UIPictures/aoi_icon.png')
        resizedAOIIcon=loadAOIIcon.resize(iconSize, Image.ANTIALIAS)
        renderAOIIcon = ImageTk.PhotoImage(resizedAOIIcon)
        AOIIconPic = Label(self.buttonFrame,image=renderAOIIcon)
        AOIIconPic.image = renderAOIIcon
        AOIIconPic.grid(row=1,column=0,padx=15,pady=5)
        AOIIconPic.bind("<Button-1>", self.aoiEvent)
        
        loadStartIcon = Image.open('UIPictures/start_icon.png')
        resizedStartIcon=loadStartIcon.resize(iconSize, Image.ANTIALIAS)
        renderStartIcon = ImageTk.PhotoImage(resizedStartIcon)
        startIconPic = Label(self.buttonFrame,image=renderStartIcon)
        startIconPic.image = renderStartIcon
        startIconPic.grid(row=1,column=1,padx=15,pady=5)
        startIconPic.bind("<Button-1>", self.startTest)
        
        self.buttonFrame.pack(pady=25)
        
        
    def startTest(self,event):
        app.PAUSE = False
        os.system('sudo python processing.py &')
        self.controller.show_frame(GUIPage)
    def cameraEvent(self,event):
        self.controller.show_frame(AlignmentCameraPage)
    def aoiEvent(self,event):
        self.controller.show_frame(AreaOfInterestPage)    
    def equationEvent(self,event):
        self.controller.show_frame(DifferenceEquationEditorPage)
        
class AlignmentCameraPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent,bg=WHITE_COLOR)
        #self.label = tk.Label(self, text="Alignment Camera", font=TITLE_FONT,fg=TEXT_COLOR,background=WHITE_COLOR)
        #self.label.grid(row=0,column=0,padx=15,pady=5)
        self.instruction_label = tk.Label(self, text="Tap Picture/nto Update", font=SMALL_FONT,fg=TEXT_COLOR,background=WHITE_COLOR)
        self.instruction_label.pack(padx=15,pady=5)
        self.timeStart = 0
        image_file = TIFF.open('PreparationUtils/View.tiff', mode='r')
        image = image_file.read_image()/256
        self.load = Image.fromarray(image)
        self.scale = .8
        self.resized=self.load.resize((int(originalImageWidth*self.scale), int(originalImageHeight*self.scale)))
        self.render = ImageTk.PhotoImage(self.resized)
        self.samplePic = Label(self,image=self.render)
        self.samplePic.image = self.render
        self.samplePic.pack(padx=15,pady=5)
        self.samplePic.bind("<Button-1>", self.updatePicture)
        
    def updatePicture(self,event):
        timeProgress = time.time() - self.timeStart
        self.timeStart = time.time()
        if timeProgress > 3:
            self.inProgress = True
            os.system("sudo python Alignment.py &")
            self.samplePic.pack_forget()
            time.sleep(1.6)
            out = 0
            image_file = TIFF.open('PreparationUtils/View.tiff', mode='r')
            image = image_file.read_image()/256
            self.load = Image.fromarray(image)
            self.resized=self.load.resize((int(originalImageWidth*self.scale), int(originalImageHeight*self.scale)))
            self.render = ImageTk.PhotoImage(self.resized)
            self.samplePic = Label(self,image=self.render)
            self.samplePic.image = self.render
            self.samplePic.pack(padx=15,pady=5)
            self.samplePic.bind("<Button-1>", self.updatePicture)
            self.inProgress = False
        
class AreaOfInterestPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent,bg=WHITE_COLOR)
        self.padyVal = 4
        self.entrySubframe = tk.Frame(self,bg=WHITE_COLOR)
        self.widthLabel = tk.Label(self.entrySubframe, text = "Width:", font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        self.widthEntry= tk.Entry(self.entrySubframe, font=LARGE_FONT,bg=TEXT_COLOR)
        self.heightLabel = tk.Label(self.entrySubframe, text = "Height:", font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        self.heightEntry = tk.Entry(self.entrySubframe, font=LARGE_FONT,bg=TEXT_COLOR)
        self.centerWLabel = tk.Label(self.entrySubframe, text = "Center (X):", font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        self.centerWEntry= tk.Entry(self.entrySubframe, font=LARGE_FONT,bg=TEXT_COLOR)
        self.centerHLabel = tk.Label(self.entrySubframe, text = "Center (Y):", font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        self.centerHEntry= tk.Entry(self.entrySubframe, font=LARGE_FONT,bg=TEXT_COLOR)
        label = tk.Label(self.entrySubframe, text="         Area of Interest Editor", font=TITLE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        label.grid(row = 0,columnspan = 2)        
        labelSpace = tk.Label(self.entrySubframe, text=" ", font=TITLE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        label.grid(row = 1,pady = 50)
        # Binding Evenets to buttons 
        self.widthEntry.bind("<Button-1>", self.showKeyboard)
        self.heightEntry.bind("<Button-1>", self.showKeyboard)
        self.widthEntry.bind("<Return>", self.updateCanvas)
        self.heightEntry.bind("<Return>", self.updateCanvas)
        self.centerWEntry.bind("<Button-1>", self.showKeyboard)
        self.centerWEntry.bind("<Return>", self.updateCanvas)
        self.centerHEntry.bind("<Button-1>", self.showKeyboard)
        self.centerHEntry.bind("<Return>", self.updateCanvas)
        # Packing
        self.centerWLabel.grid(row=4,pady=10)
        self.centerWEntry.grid(row=4,column=1,pady=10)
        self.centerHLabel.grid(row=5,pady=10)
        self.centerHEntry.grid(row=5,column=1,pady=10)
        self.widthLabel.grid(row=6,pady=10)
        self.widthEntry.grid(row=6,column=1,pady=10)
        self.heightLabel.grid(row=7,pady=10)
        self.heightEntry.grid(row=7,column=1,pady=10)
        #scaling factor of picture
        self.scaleDownBy = 2
        self.scale = 1/self.scaleDownBy
        self.scaledImageWidth = originalImageWidth / self.scaleDownBy
        self.scaledImageHeight = originalImageHeight / self.scaleDownBy
        self.centerImageWidth = int(self.scaledImageWidth/2)
        self.centerImageHeight = int(self.scaledImageHeight/2)
        image_file = TIFF.open('PreparationUtils/View.tiff', mode='r')
        image = image_file.read_image()/256
        self.load = Image.fromarray(image)
        self.resized = self.load.resize((self.scaledImageWidth, self.scaledImageHeight))
        self.render = ImageTk.PhotoImage(self.resized)
        self.canvasFrame = tk.Frame(self,bg=WHITE_COLOR)
        self.canvas = Canvas(self.canvasFrame, width=self.resized.size[0], height=self.resized.size[1])
        self.canvas.create_image(0,0,anchor=NW,image=self.render)
        self.rectangleDrawn = self.canvas.create_rectangle(0,0,self.scaledImageWidth,self.scaledImageHeight,outline=WHITE_COLOR,fill='grey',stipple='@GraphingAssets/transparent.xbm',width=2)
        self.canvas.pack()
        self.entrySubframe.grid(row = 0, column = 0, sticky="nsew",pady=50)
        self.canvasFrame.grid(row = 0, column = 1, sticky="nsew",pady=50,padx=40)
        x1, y1 = (self.scaledImageWidth/2 - 2), (self.scaledImageHeight/2 - 2)
        x2, y2 = (self.scaledImageWidth/2 + 2), (self.scaledImageHeight/2 + 2)
        self.centerDrawn = self.canvas.create_oval(x1, y1, x2, y2, fill=WHITE_COLOR)
        self.currentCenterLabel = Label(self.entrySubframe, text = "Image Center X: " + str(self.scaledImageWidth) + "\n\n Image Center Y: "+ str(self.scaledImageHeight), font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        self.currentDimLabel = Label(self.entrySubframe, text = "Image Width: " + str(self.scaledImageWidth*2) + "\n\n Image Height: "+ str(self.scaledImageHeight*2), font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        self.currentCenterLabel.grid(row=9,column = 1,pady=10)
        self.currentDimLabel.grid(row=10,column = 1,pady=10)
        #button frame
        self.buttonSubframe = tk.Frame(self.entrySubframe,bg=WHITE_COLOR)
        self.buttonSubframe.grid(row = 8,column = 1)
        # submit button
        self.submit_button = Button(self.buttonSubframe, font = SMALLBUTTON_FONT, highlightthickness = 0, image=controller.buttonBackgroundSmall,compound=CENTER, text="Submit",command=self.saveAreaOfInterest,background=WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        self.submit_button.pack(side = tk.LEFT, padx=20)
        # info label
        infoLabel = tk.Label(self.canvasFrame, text="Note: The image shown is scaled by 1/2.\n\nThe image area shown in the blue box is still the\n\narea which will be analysed in the non-scaled image.", font=LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        infoLabel.pack(pady=15)  
        
    def showKeyboard(self,event):
        os.system("killall matchbox-keyboard")
        os.system("matchbox-keyboard &")
    def updateCanvas(self,event):
        if ((self.centerWEntry.get() != 0) and(self.centerHEntry.get() != 0) and (self.widthEntry.get() != 0) and (self.heightEntry.get() != 0)):
            centerW = int(int(self.centerWEntry.get())/2)
            centerH = int(int(self.centerHEntry.get())/2)
            x1, y1 = (centerW - 1), (centerH - 1)
            x2, y2 = (centerW + 1), (centerH + 1)
            width = int(self.widthEntry.get())
            height = int(self.heightEntry.get())
            widthLeft = int(centerW - width/2)
            heightLeft = int(centerH - height/2)
            widthRight = int(centerW + width/2)
            heightRight = int(centerH + height/2)
            self.canvas.delete(self.rectangleDrawn)
            self.canvas.delete(self.centerDrawn)
            self.centerDrawn = self.canvas.create_oval(x1, y1, x2, y2, fill=WHITE_COLOR)
            self.rectangleDrawn = self.canvas.create_rectangle(widthLeft-1,heightLeft-1,widthRight,heightRight,outline=WHITE_COLOR,fill='grey',stipple='@GraphingAssets/transparent.xbm',width=1)
            self.widthLeft =  widthLeft
            self.widthRight = widthRight
            self.heightLeft = heightLeft
            self.heightRight = heightRight
    def saveAreaOfInterest(self):
        noEvent = 0
        self.updateCanvas(noEvent)
        writeToTextFile("Equations/aoi.txt",str(self.widthLeft)+"\n"+str(self.heightLeft)+"\n"+str(self.widthRight)+"\n"+str(self.heightRight))


class DifferenceEquationEditorPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent,bg=WHITE_COLOR)
        self.padyVal = 4
        # left and right frame
        self.leftFrame = tk.Frame(self,bg=WHITE_COLOR)
        self.rightFrame = tk.Frame(self,bg=WHITE_COLOR)
        # equation entry 
        self.title = tk.Label(self.leftFrame, text = "Difference Equation Editor", font = TITLE_FONT,bg = WHITE_COLOR,fg=TEXT_COLOR)
        self.legend = tk.Label(self.leftFrame, text = "For equation use:\n X for first Laser \n Y for second Laser\n\n Note:\nVariables must be capitalized!\nMultiplication Symbol (*) is never assumed!\n Example: 2X must be typed as 2*X", font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        self.numeratorEntryLabel = tk.Label(self.leftFrame, text = "\nEnter the numerator portion of difference equation: ", font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        self.denominatorEntryLabel = tk.Label(self.leftFrame, text = "Enter the denominator portion of difference equation:", font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        self.numeratorEntry = tk.Entry(self.leftFrame, font=LARGE_FONT,bg=TEXT_COLOR)
        self.denominatorEntry = tk.Entry(self.leftFrame, font=LARGE_FONT,bg=TEXT_COLOR)
        self.numeratorEntry.bind("<Button-1>", self.showKeyboard)
        self.denominatorEntry.bind("<Button-1>", self.showKeyboard)
        
        self.title.pack()
        self.numeratorEntryLabel.pack(pady=self.padyVal)
        self.numeratorEntry.pack(pady=self.padyVal)
        self.denominatorEntryLabel.pack(pady=self.padyVal)
        self.denominatorEntry.pack(pady=self.padyVal)
        
        #button frame
        self.subframe = tk.Frame(self.leftFrame,bg=WHITE_COLOR)
        self.subframe.pack(side="top",pady=self.padyVal)
        
        # submit button
        self.submit_button = Button(self.subframe,  font = SMALLBUTTON_FONT, highlightthickness = 0, image=controller.buttonBackgroundSmall,compound=CENTER, text="Submit",command=lambda: self.equationEditorSave(controller),background=WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        self.submit_button.pack(side = tk.LEFT, padx=20)
        
        
        # inserting picture
        self.updateEquationShown()
        self.load = Image.open('UIPictures/lasersetuplabeled.png')
        self.resized=self.load.resize((475, 400), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(self.resized)
        self.laserSetupPic = Label(self.rightFrame,image=self.render)
        self.laserSetupPic.image = self.render
        self.laserSetupPic.pack()
        self.legend.pack()
        self.leftFrame.grid(row = 0,padx = 100,pady=25)
        self.rightFrame.grid(row = 0, column = 1)
        
    def updateEquationShown(self):
        self.legend.pack_forget()
        
        numeratorSaved = readTextFile("Equations/numerator.txt")
        denominatorSaved = readTextFile("Equations/denominator.txt")
        self.savedLabel = Label(self.leftFrame, text = "Currently Saved Equation: \n", font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        self.numeratorSavedLabel = Label(self.leftFrame, text = numeratorSaved, font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        self.denominatorSavedLabel = Label(self.leftFrame, text = denominatorSaved, font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        self.spaceSaved = Label(self.leftFrame, text = "_________________", font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        
        self.savedLabel.pack(pady=self.padyVal)
        self.numeratorSavedLabel.pack()
        self.spaceSaved.pack()
        self.denominatorSavedLabel.pack(side = tk.TOP, pady = 18)
        self.legend.pack()
        
    def equationEditorSave(self,controller):
        
        writeToTextFile("Equations/numerator.txt",self.numeratorEntry.get())
        writeToTextFile("Equations/denominator.txt",self.denominatorEntry.get())
        # destroying the current labels so the repack works
        self.savedLabel.destroy()
        self.numeratorSavedLabel.destroy()
        self.denominatorSavedLabel.destroy()
        self.spaceSaved.destroy()
        self.updateEquationShown()
        
        self.repack()
    def repack(self): # call whenever information has been refreshed been refreshed to reorient screen correctly for the equation editor page
        # forgetting current pack
        self.leftFrame.grid_forget()
        self.rightFrame.grid_forget()
        # packing page
        self.leftFrame.grid(row = 0)
        self.rightFrame.grid(row = 0, column = 1)
        
        
    def showKeyboard(self,event):
        os.system("killall matchbox-keyboard")
        os.system("matchbox-keyboard &")

class GUIPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent,bg=WHITE_COLOR)
        self.controller = controller
        label = tk.Label(self, text="GUI", font=TITLE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        label.pack(pady=10,padx=10)
        self.controller=controller
        buttonFrame = Frame(self,bg=WHITE_COLOR)       
        switch_button = tk.Button(buttonFrame, font = LARGE2_FONT, highlightthickness = 0, image=controller.buttonBackground,compound=CENTER, text="View the Sample",command=self.showPicDisplay,background=WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        switch_button.grid(row=0,column=0,padx=10)
        self.pause_button = tk.Button(buttonFrame, font = LARGE2_FONT, highlightthickness = 0, image=controller.buttonBackground,compound=CENTER, text="Pause Graph",command=self.pauseAnimation,background=WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        self.pause_button.grid(row=0,column=1)
        self.resume_button= tk.Button(buttonFrame, font = LARGE2_FONT, highlightthickness = 0, image=controller.buttonBackground,compound=CENTER,text="Resume Graph",command=self.resumeAnimation,background=WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        save_button = tk.Button(buttonFrame, font = LARGE2_FONT, highlightthickness = 0, image=controller.buttonBackground,compound=CENTER, text="Save and Exit Test",command=self.endTest,background=WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        save_button.grid(row=0,column=2,padx=10)
        buttonFrame.pack()
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = 1)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
    def pauseAnimation(self):
        app.PAUSE = True
        self.pause_button.grid_forget()
        self.resume_button.grid(row=0,column=1,padx=10)
    def resumeAnimation(self):
        app.PAUSE = False
        self.resume_button.grid_forget()
        self.pause_button.grid(row=0,column=1,padx=10)
    def showPicDisplay(self):
        self.pauseAnimation()
        self.controller.show_frame(PictureDisplayPage)
    def endTest(self):
        turnOffProcessor()
        answer = tkMessageBox.showinfo('Saving', message = 'Saving... Please do not touch device.', icon = 'warning')
        transferDataToStorage()
        self.controller.backToStartPage()


   
class PictureDisplayPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent,bg=WHITE_COLOR)
        label = tk.Label(self, text="Sample Picture Display", font=TITLE_FONT,fg=TEXT_COLOR,background=WHITE_COLOR)
        label.pack(pady=10, padx=10)
        switch_button = tk.Button(self, font = LARGE2_FONT, highlightthickness = 0, image=controller.buttonBackground,compound=CENTER, text="View Graphical Data",command=lambda: controller.show_frame(GUIPage),background=WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        switch_button.pack()  
        
        image_file = TIFF.open('PreparationUtils/View.tiff', mode='r')
        image = image_file.read_image()/256
        self.load = Image.fromarray(image)
        self.scale = .65
        self.resized=self.load.resize((int(originalImageWidth*self.scale), int(originalImageHeight*self.scale)))
        self.render = ImageTk.PhotoImage(self.resized)
        self.samplePic = Label(self,image=self.render)
        self.samplePic.image = self.render
        self.samplePic.pack()
        self.samplePic.bind("<Button-1>", self.updatePicture)
    def showGraph(self):
        app.PAUSE = False
        self.controller.show_frame(PictureDisplayPage)
    def updatePicture(self,event):
        self.samplePic.pack_forget()
        time.sleep(1.6)
        out = 0 
        while(out == 0):
            try:
                latest_file = max(list_of_files,key=os.path.getctime)
                out = 1
            except:
                list_of_files = glob.glob('Biosensor_Images/*')
        out = 0
        while(out==0):
            try:
                image_file = TIFF.open(latest_file, mode='r')
                out = 1
            except:
                out = 0
        image = image_file.read_image()/256
        self.load = Image.fromarray(image)
        self.scale = .65
        self.resized=self.load.resize((int(originalImageWidth*self.scale), int(originalImageHeight*self.scale)))
        self.render = ImageTk.PhotoImage(self.resized)
        self.samplePic = Label(self,image=self.render)
        self.samplePic.image = self.render
        self.samplePic.pack()
        self.samplePic.bind("<Button-1>", self.updatePicture)

def writeToTextFile(nameOfFile,textToBeSaved): # writes over the current text file with the input information
    file = open(nameOfFile,"w")
    file.write(textToBeSaved)
    file.close()
def readTextFile(nameOfFile): # reads the text file and return the resulting information in whole
    readText = (open(nameOfFile,"r").read())
    return readText
def turnOffProcessor():
    writeToTextFile('Data/processorState.txt','0')
def turnOnProcessor():
    writeToTextFile('Data/processorState.txt','1')
def turnOffCamera():
    writeToTextFile('Data/cameraState.txt','0')
def turnOnCamera():
    writeToTextFile('Data/cameraState.txt','1')    

def transferDataToStorage():
    os.system("sudo cp -r Biosensor_Images /media/pi/EXTSTORAGE/Portable_Biosensor_Data/.")
    os.system("sudo rm Biosensor_Images/*.tiff")
    os.system("sudo cp -r Data /media/pi/EXTSTORAGE/Portable_Biosensor_Data/.")




app = PortableBiosensorUI()
ani = animation.FuncAnimation(f, animate, interval=10000)
#cameraAnimations = animation.FuncAnimation(f,updateImage,interval=5000)

# interval is in milliseconds, interval set to 20 second (20000 ms)
app.mainloop()
turnOffProcessor()
transferDataToStorage()


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
