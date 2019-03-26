''' INFORMATION#
Using Python 2
Must start program from sudo user to write successfully
to run navigate to SampleUI file in terminal and launch with "sudo python main.py &"
Whenever adding a new page, must add it to container class

TODO
add videos
'''
import matplotlib
import os
import time
from libtiff import TIFF
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import Tkinter as tk
import tkFont
import ttk
from ttk import *
import tkMessageBox
from Tkinter import *
from PIL import Image, ImageTk





originalImageWidth = 1288
originalImageHeight = 964
BORDERWIDTH = 0.0
BLUE_COLOR = '#3f88bf'
WHITE_COLOR = '#1D69A4' # Red = 29  Green = 105  Blue = 164
TEXT_COLOR = '#ffffff'
BUTTON_COLOR = '#1D69A4'

TITLE_FONT = ("Arial", 24)
LARGE_FONT = ("Arial", 16)
SMALL_FONT = ("Arial", 8)
style.use("ggplot")
iconSize = (275,275)
buttonSize = (175,30)
buttonSizeSmall = (100,30)

#mostRecentPhotoName = 'Biosensor_Images/880nm_12in.tif'
#mostRecentPhotoFigure = Figure(figsize=(5,5), dpi=100)

f = Figure(figsize=(5,5), dpi=100)
rawPlot = f.add_subplot(121) # 121 = 1x2 figure plot number 1
processedPlot = f.add_subplot(122) # 121 = 1x2 figure plot number 2


# animation function for displaying graphs
def animate(i):
    if app.PAUSE == False:
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
                        xList1.append(int(x))
                        yList1.append(float(y))
                    if(laserNumber==2):
                        xList2.append(int(x))
                        yList2.append(float(y))
                    if(laserNumber==3):   
                        xList3.append(int(x))
                        yList3.append(float(y))
        rawPlot.scatter(xList1, yList1, color = 'r')
        rawPlot.scatter(xList2, yList2, color = '#ffff05')
        rawPlot.scatter(xList3, yList3, color = 'b')
        
        pullDataProcessed = []
        pullDataProcessed.append(open("Data/processedData.txt","r").read())
        i = 1
        processedPlot.clear()
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
                    x, y,laserNumberTxt,filename = eachLine.split(',')
                    laserNumber = int(laserNumberTxt)
                    if(laserNumber==12):
                        xList12.append(int(x))
                        yList12.append(float(y))
                    if(laserNumber==23):
                        xList23.append(int(x))
                        yList23.append(float(y))  
                    if(laserNumber==31):
                        xList31.append(int(x))
                        yList31.append(float(y))
        processedPlot.scatter(xList12, yList12, color = '#ffa500')
        processedPlot.scatter(xList23, yList23, color = 'g')
        processedPlot.scatter(xList31, yList31, color = 'm')
        
        rawPlot.set_ylim([0,66000])
        rawPlot.set_xlim([0,len(xList1)+1])
        processedPlot.set_ylim([0,66000])
        processedPlot.set_xlim([0,len(xList12)+1])
        rawPlot.set_title('Raw Data')
        processedPlot.set_title('Difference Equation Data')
'''def updateImage(i):
    if app.PauseFeed == false:
        counterGlobal++
        file = open()
        
'''
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
            
        menu = tk.Menu(self,bg = "blue",fg=TEXT_COLOR)
        self.config(menu=menu)
        menu.add_command(label="Start Page", command = self.backToStartPage)
        self.show_frame(StartPage)
    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise() # raises the frame to the front
        
    def backToStartPage(self):
        answer = tkMessageBox.askquestion('Return to Start Page', message = 'Are you sure you want to return to start page?', icon = 'warning')
        if answer == 'yes':
            app.PAUSE = True
            self.show_frame(StartPage)
# Lambda function: quick throw away function to allow us to pass arguements with function to command= in button

# Pages
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent,bg=WHITE_COLOR)
        label = tk.Label(self,text="Welcome to the Portable Biosensor UI!", font=TITLE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        label.pack(pady=10, padx=10)
        
        self.subframe = tk.Frame(self,bg=WHITE_COLOR)
        self.subframe.pack(side="top",padx=250,pady = 50)
        help_button = tk.Button(self.subframe, highlightthickness = 0, image=controller.buttonBackground,text="Need Help?",borderwidth=BORDERWIDTH,compound=CENTER,command=lambda: controller.show_frame(HelpPage),background=BUTTON_COLOR,foreground=TEXT_COLOR)
        help_button.pack(side=tk.LEFT,padx=15)
        testPrep_button = tk.Button(self.subframe, highlightthickness = 0, image=controller.buttonBackground,compound=CENTER,text="Start Test Preperation",command=lambda: controller.show_frame(TestPrepPage),background=BUTTON_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
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
        
        instructionsLabel = tk.Label(self,text="Select desired option and hit Start Test when ready", font=LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        instructionsLabel.pack(pady=20)
        
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
        AOIIconPic.grid(row=0,column=2,padx=15,pady=5)
        AOIIconPic.bind("<Button-1>", self.aoiEvent)
        
        loadStartIcon = Image.open('UIPictures/start_icon.png')
        resizedStartIcon=loadStartIcon.resize(iconSize, Image.ANTIALIAS)
        renderStartIcon = ImageTk.PhotoImage(resizedStartIcon)
        startIconPic = Label(self.buttonFrame,image=renderStartIcon)
        startIconPic.image = renderStartIcon
        startIconPic.grid(row=0,column=3,padx=15,pady=5)
        startIconPic.bind("<Button-1>", self.startTest)
        
        self.buttonFrame.pack(pady=100)
        
        
    def startTest(self,event):
        app.PAUSE = False
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
        label = tk.Label(self, text="Alignment Camera", font=TITLE_FONT,fg=TEXT_COLOR,background=WHITE_COLOR)
        label.pack(pady=10, padx=15)
        back_button = tk.Button(self, highlightthickness = 0, image=controller.buttonBackgroundSmall,compound=CENTER, text="Return",command=lambda: controller.show_frame(TestPrepPage),background=WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        back_button.pack(pady=15)
        image_file = TIFF.open('Biosensor_Images/880nm_12in.tif', mode='r')
        image = image_file.read_image()/256
        self.load = Image.fromarray(image)
        self.scale = .60
        self.resized=self.load.resize((int(originalImageWidth*self.scale), int(originalImageHeight*self.scale)))
        self.render = ImageTk.PhotoImage(self.resized)
        self.samplePic = Label(self,image=self.render)
        self.samplePic.image = self.render
        self.samplePic.pack()
        
        
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
        
        
        
        self.widthEntry.bind("<Button-1>", self.showKeyboard)
        self.heightEntry.bind("<Button-1>", self.showKeyboard)
        self.widthEntry.bind("<Return>", self.updateCanvas)
        self.heightEntry.bind("<Return>", self.updateCanvas)
        self.centerWEntry.bind("<Button-1>", self.showKeyboard)
        self.centerWEntry.bind("<Return>", self.updateCanvas)
        self.centerHEntry.bind("<Button-1>", self.showKeyboard)
        self.centerHEntry.bind("<Return>", self.updateCanvas)
        
        
        self.centerWLabel.grid(row=4,pady=10)
        self.centerWEntry.grid(row=4,column=1,pady=10)
        self.centerHLabel.grid(row=5,pady=10)
        self.centerHEntry.grid(row=5,column=1,pady=10)
        self.widthLabel.grid(row=6,pady=10)
        self.widthEntry.grid(row=6,column=1,pady=10)
        self.heightLabel.grid(row=7,pady=10)
        self.heightEntry.grid(row=7,column=1,pady=10)
        
        # currentCenterCoordinatesLabel = Label(self.entrySubframe, text = "",font=LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        

        
        #scaling factor of picture
        self.scaleDownBy = 2
        self.scale = 1/self.scaleDownBy
        self.scaledImageWidth = originalImageWidth / self.scaleDownBy
        self.scaledImageHeight = originalImageHeight / self.scaleDownBy
        self.centerImageWidth = int(self.scaledImageWidth/2)
        self.centerImageHeight = int(self.scaledImageHeight/2)
        image_file = TIFF.open('Biosensor_Images/880nm_12in.tif', mode='r')
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
        self.canvasFrame.grid(row = 0, column = 1, sticky="nsew",pady=50,padx=70)
        x1, y1 = (self.scaledImageWidth/2 - 2), (self.scaledImageHeight/2 - 2)
        x2, y2 = (self.scaledImageWidth/2 + 2), (self.scaledImageHeight/2 + 2)
        self.centerDrawn = self.canvas.create_oval(x1, y1, x2, y2, fill=WHITE_COLOR)
        self.currentCenterLabel = Label(self.entrySubframe, text = "Image Center X: " + str(self.scaledImageWidth/2) + "\n\n Image Center Y: "+ str(self.scaledImageHeight/2), font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        self.currentDimLabel = Label(self.entrySubframe, text = "Image Width: " + str(self.scaledImageWidth) + "\n\n Image Height: "+ str(self.scaledImageHeight), font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        self.currentCenterLabel.grid(row=9,column = 1,pady=10)
        self.currentDimLabel.grid(row=10,column = 1,pady=10)
        
        #button frame
        self.buttonSubframe = tk.Frame(self.entrySubframe,bg=WHITE_COLOR)
        self.buttonSubframe.grid(row = 8,column = 1)
        
        # submit button
        self.submit_button = Button(self.buttonSubframe, highlightthickness = 0, image=controller.buttonBackgroundSmall,compound=CENTER, text="Submit",command=self.saveAreaOfInterest,background=WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        self.submit_button.pack(side = tk.LEFT, padx=20)
        
        # return button
        self.return_button = Button(self.buttonSubframe, highlightthickness = 0, image=controller.buttonBackgroundSmall,compound=CENTER, text="Return",command=lambda: controller.show_frame(TestPrepPage),background = WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        self.return_button.pack(side = tk.LEFT, padx=20)
        
        # info label
        infoLabel = tk.Label(self.canvasFrame, text="Note: The image shown is scaled by 1/2.\n\nThe image area shown in the blue box is still the\n\narea which will be analysed in the non-scaled image.", font=LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        infoLabel.pack(pady=15)  
        
    def showKeyboard(self,event):
        os.system("killall matchbox-keyboard")
        os.system("matchbox-keyboard &")
    def updateCanvas(self,event):
        
        if ((self.centerWEntry.get() != 0) and(self.centerHEntry.get() != 0) and (self.widthEntry.get() != 0) and (self.heightEntry.get() != 0)):
            
            centerW = int(self.centerWEntry.get())
            centerH = int(self.centerHEntry.get())
            
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
        writeToTextFile("Equations/aoi.txt",str(self.scaleDownBy*self.widthLeft)+"\n"+str(self.scaleDownBy*self.heightLeft)+"\n"+str(self.scaleDownBy*self.widthRight)+"\n"+str(self.scaleDownBy*self.heightRight))
        



class DifferenceEquationEditorPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent,bg=WHITE_COLOR)
        self.padyVal = 4
        
        # left and right frame
        self.leftFrame = tk.Frame(self,bg=WHITE_COLOR)
        self.rightFrame = tk.Frame(self,bg=WHITE_COLOR)
        
        # equation entry 
        self.title = tk.Label(self.leftFrame, text = "\nDifference Equation Editor", font = TITLE_FONT,bg = WHITE_COLOR,fg=TEXT_COLOR)
        self.legend = tk.Label(self.leftFrame, text = "For equation use:\n X for first Laser \n Y for second Laser\n\n Note:\nVariables must be capitolized!\nMultiplication Symbol (*) is never assumed!\n Example: 2X must be typed as 2*X", font = LARGE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
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
        self.subframe.pack(side="top",padx=250,pady=self.padyVal)
        
        # submit button
        self.submit_button = Button(self.subframe, highlightthickness = 0, image=controller.buttonBackgroundSmall,compound=CENTER, text="Submit",command=lambda: self.equationEditorSave(controller),background=WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        self.submit_button.pack(side = tk.LEFT, padx=20)
        
        # return button
        self.return_button = Button(self.subframe, highlightthickness = 0, image=controller.buttonBackgroundSmall,compound=CENTER, text="Return",command=lambda: controller.show_frame(TestPrepPage),background = WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        self.return_button.pack(side = tk.LEFT, padx=20)
        
        # inserting picture
        self.updateEquationShown()
        self.load = Image.open('UIPictures/lasersetuplabeled.png')
        self.resized=self.load.resize((475, 400), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(self.resized)
        self.laserSetupPic = Label(self.rightFrame,image=self.render)
        self.laserSetupPic.image = self.render
        self.laserSetupPic.pack()
        self.legend.pack()
        self.leftFrame.grid(row = 0)
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
        label = tk.Label(self, text="GUI", font=TITLE_FONT,bg=WHITE_COLOR,fg=TEXT_COLOR)
        label.pack(pady=10,padx=10)
        self.controller=controller
        buttonFrame = Frame(self,bg=WHITE_COLOR)       
        switch_button = tk.Button(buttonFrame, highlightthickness = 0, image=controller.buttonBackground,compound=CENTER, text="View the Sample",command=self.showPicDisplay,background=WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        switch_button.grid(row=0,column=0,padx=10)
        self.pause_button = tk.Button(buttonFrame, highlightthickness = 0, image=controller.buttonBackground,compound=CENTER, text="Pause Graph",command=self.pauseAnimation,background=WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        self.pause_button.grid(row=0,column=1)
        self.resume_button= tk.Button(buttonFrame, highlightthickness = 0, image=controller.buttonBackground,compound=CENTER,text="Resume Graph",command=self.resumeAnimation,background=WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
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


   
class PictureDisplayPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent,bg=WHITE_COLOR)
        label = tk.Label(self, text="Sample Picture Display", font=TITLE_FONT,fg=TEXT_COLOR,background=WHITE_COLOR)
        label.pack(pady=10, padx=10)
        switch_button = tk.Button(self, highlightthickness = 0, image=controller.buttonBackground,compound=CENTER, text="View Graphical Data",command=lambda: controller.show_frame(GUIPage),background=WHITE_COLOR,foreground=TEXT_COLOR,borderwidth=BORDERWIDTH)
        switch_button.pack()  
        
        image_file = TIFF.open('Biosensor_Images/880nm_12in.tif', mode='r')
        image = image_file.read_image()/256
        self.load = Image.fromarray(image)
        self.scale = .65
        self.resized=self.load.resize((int(originalImageWidth*self.scale), int(originalImageHeight*self.scale)))
        self.render = ImageTk.PhotoImage(self.resized)
        self.samplePic = Label(self,image=self.render)
        self.samplePic.image = self.render
        self.samplePic.pack()
    def showGraph(self):
        app.PAUSE = False
        self.controller.show_frame(PictureDisplayPage)
        

def writeToTextFile(nameOfFile,textToBeSaved): # writes over the current text file with the input information
    file = open(nameOfFile,"w")
    file.write(textToBeSaved)
    file.close()
def readTextFile(nameOfFile): # reads the text file and return the resulting information in whole
    readText = (open(nameOfFile,"r").read())
    return readText
    




app = PortableBiosensorUI()
ani = animation.FuncAnimation(f, animate, interval=5000)
#cameraAnimations = animation.FuncAnimation(f,updateImage,interval=5000)

# interval is in milliseconds, interval set to 20 second (20000 ms)
app.mainloop()

def qf(stringtoprint):
    print(stringtoprint)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    