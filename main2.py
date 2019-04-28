from Tkinter import *
import threading
import tkMessageBox
# Raspberry Pi login -> Uname: pi     Password: Sicem1996
# User/Password menu
''' class Credintials:
    def __init__(self,master):
        frame = Frame(master)
        self.master = master
        master.title("Login")
        frame.grid(row = 0)
        profile_name_label = Label(root, text = "Profile Name: ")
        profile_password_label = Label(root, text = "Password: ")
        profile_name_entry = Entry(root)
        profile_password_entry = Entry(root)

        profile_name_label.grid(row = 0, sticky=E)
        profile_password_label.grid(row = 1, sticky=E)
        profile_name_entry.grid(row = 0, column = 1)
        profile_password_entry.grid(row = 1, column = 1)

        c = Checkbutton(root, text='Keep me logged in')
        c.grid(columnspan = 2)

        submit_button = Button(root, text="Submit",command=self.master.destroy)

        #submit_button.bind("<Button-1>",command = self.frame.quit)
        #<Button-1> is the event of left mouse click
        submit_button.grid(row = 3)
        '''
class Graphical_interface_help_menu:
    def __init__(self,master):
        self.master = master
        master.geometry('800x800')
        master.title("Main Menu")
        master.configure(background = "dark green")
        frame = Frame(master)
        menu = Menu(master,bg = "blue")
        master.config(menu=menu)
        bottomframe = Frame(master)
        bottomframe.pack(side = BOTTOM)
        helpButton1 = Button(toolbar,text="Preparing the Sample",command =self.Do_nothing)
        helpButton1.pack(side=TOP, padx=2,pady=2)
        helpButton2 = Button(toolbar,text="Loading the Sample",command =self.Do_nothing)
        helpButton2.pack(side=TOP, padx=2,pady=2)
        helpButton3 = Button(toolbar,text="Defining Area of Interest",command =self.Do_nothing)
        helpButton3.pack(side=TOP, padx=2,pady=2)
        helpButton4 = Button(toolbar,text="Understanding Graph",command =self.Do_nothing)
        helpButton4.pack(side=TOP, padx=2,pady=2)
        helpButton5 = Button(toolbar,text="Exporting Data",command =self.Do_nothing)
        helpButton5.pack(side=TOP, padx=2,pady=2)
        helpButton6 = Button(toolbar,text="Return to Main Menu",command =self.Do_nothing)
        helpButton6.pack(side=TOP, padx=2,pady=2)
    def Do_nothing(self):
        print("doing nothing")
# Main Menu
# can define inheritance in class like: Graphical_interface(tk.TK):
class Graphical_interface:  # Program Container Class
    def __init__(self,master):
        self.master = master
        master.geometry('800x800')
        master.title("Main Menu")
        master.configure(background = "dark green")
        frame = Frame(master)
        menu = Menu(master,bg = "blue")
        master.config(menu=menu)
        bottomframe = Frame(master)
        bottomframe.pack(side = BOTTOM)
        
        conMenu = Menu(menu)
        subMenu = Menu(menu)
        menu.add_cascade(label="Action", menu=subMenu)
        menu.add_cascade(label="Configuration", menu=conMenu)
        
        subMenu.add_command(label="Exit", command=self.master.destroy)
        subMenu.add_separator()
        subMenu.add_command(label="Start Process", command=self.Make_shape)
        subMenu.add_command(label="Clear Graph",command=self.Clear_graph)
        subMenu.add_command(label="Load Previous Test",command=self.Load_image)
        subMenu.add_command(label="Clear Previous Test",command=self.Clear_image)
        
        conMenu.add_command(label="Filter 1",command=self.Do_nothing)
        conMenu.add_command(label="Filter 2",command=self.Do_nothing)
        conMenu.add_command(label="Filter 3",command=self.Do_nothing)
        conMenu.add_separator()
        conMenu.add_command(label="Create New Filter",command=self.Do_nothing)
        
        
        '''#Toolbar
        toolbar = Frame(self.master, bg="blue")
        zoomButton = Button(toolbar,text="Zoom In",command =self.Do_nothing)
        zoomButton.pack(side=LEFT, padx=2,pady=2)#padx or pady inserts space in between button = number of pixels
        saveButton = Button(toolbar,text="Save",command =self.Save_method)
        saveButton.pack(side=LEFT, padx=2,pady=2)
        toolbar.pack(side=TOP, fill=X)
        #fill=X means it will expand in x direction, but not y.
        '''
        # Welcome Text
        welcome_text = Text(self.master,font=("Helvetica",22), bg = "gold3",bd = "0")
        welcome_text.insert(INSERT, "Welcome To The Portable Biosensor!")
        welcome_text.pack(anchor = "sw", padx = 150, pady = 300)
        #welcome_text.tag_add("here", "1.0", "1.10000000")
        #welcome_text.tag_add("start", "1.8", "1.13")
        #welcome_text.tag_config("here",background="yellow",foreground="blue")
        #welcome_text.tag_config("start",background="black",foreground="green")
        
      
        # Status Bar
        status = Label(self.master, text="Saved",bd=1, relief=SUNKEN, anchor=W)
        self.status = status
        
        #setting up central canvas
        canvas= Canvas(self.master, width=500, height=500)
        self.canvas = canvas
        self.canvas.pack()
        
        start_test_button = Button(bottomframe, text = "Start Preperation for Test",font=("Helvetica",22),fg = "gold2")
        start_test_button.pack(side = BOTTOM)
        
        
        
    def Do_nothing(self):
        print("doing nothing")
    def Save_method(self):
        save_status = tkMessageBox.askquestion('Save',message='Do you want to save your program?')
        if save_status == 'yes':
            self.status.pack(side=BOTTOM)
    def Make_shape(self):
        self.canvas.delete(ALL)
        greenBox = self.canvas.create_rectangle(200,200,400,400,fill='green')
        blackLine = self.canvas.create_line(200,200,400,400)
        redline = self.canvas.create_line(400,200,200,400, fill='red')
    def Clear_graph(self):
        self.canvas.delete(ALL)
    def Load_image(self):
        self.canvas.delete(ALL)
        photo = PhotoImage(file="/home/jamesbous/Image_0077.PNG")
        self.photo = photo
        self.canvas.create_image(50,50,anchor=NW, image=self.photo)
    def Clear_image(self):
        self.canvas.delete(ALL)
        
        
        
        

primary = Tk()
graph_class = Graphical_interface(primary)
root = Toplevel()
# credinitial_class = Credintials(root)
root.mainloop()
primary.mainloop()
