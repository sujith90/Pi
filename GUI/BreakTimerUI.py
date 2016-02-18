import Tkinter as tk
from BreakTimer import BreakTimer
from _functools import partial
import threading
import datetime as dt
import time
import sys
from thermaldisplay import Tracking
from LedControl import LedControl
from MonkeyControl import MonkeyControl
import traceback
import RPi.GPIO as GPIO



class BreakScreen(tk.Frame):
    #This Page corresponds to the Break Screen
    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        
        self.grid()
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)

class SettingsGeneralSceen(tk.Frame):
    #This page corresponds to the General Settings Screen
    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        top=self.winfo_toplevel()

class SettingsETSReminderScreen(tk.Frame):
    #This page corresponds to the ETS Reminder Settings Screen
    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        top=self.winfo_toplevel()
        # top.rowconfigure(0,weight=1)
        # top.columnconfigure(0,weight=1)
        # top.rowconfigure(1,weight=1)
        # top.columnconfigure(1,weight=1)
        # top.rowconfigure(2,weight=1)
        # top.columnconfigure(2,weight=1)
        
class SettingsBreakReminderScreen(tk.Frame):
    #This page corresponds to the Break Reminder Settings Screen
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        top=self.winfo_toplevel()


class Application(tk.Frame):
    #This is the main application
    def __init__(self,master=None):
	print "GUI Init started...\n"
        #Creates Main Frame
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W) #Create main Grid of the application
        
        global breakTimerInstance #This lets the object work in another thread
        self.breakTimerInstance = BreakTimer() # instance of BreakTimer from BreakTimer.py

        
        #Active screen flags
        self.isMainScreenActive                     =   False
        self.isBreakScreenActive                    =   False
        self.isSettingsGeneralScreenActive          =   False
        self.isSettingsETSScreenActive              =   False
        self.isSettingsBreakReminderScreenActive    =   False
        
        #All Thread Exit flag
        self.allThreadExit = False

	
        
        #Create the screens
        self.initCreateMainScreen()
        self.initCreateBreakScreen()
        self.initSettingsETSReminderScreen() #This function creates the dictionaries so it must go before the other Settings Screens
        self.initSettingsGeneralScreen()
        self.initSettingsBreakReminderScreen()
        
        #Initialize Settings
        self.breakTimerInstance.loadSettings()
        if self.breakTimerInstance.getIsSettingsDefault() != True:
            self.savedSettings = self.breakTimerInstance.getSavedSettings()
            index = 0
            for each in self.stringVarsDict:
                self.stringVarsDict[each].set(self.savedSettings[each])
                index+=1
        else:
            self.savedSettings = self.breakTimerInstance.getDefaultSettings()
            
        if self.savedSettings[self.breakTimerInstance.getSettingsDeactivateMonkeyKey()] == "1":
            self.monkeyCheckButton.select()
            

	#Initialize LED Control Instance
	global ledControlInstance
	self.ledControlInstance = LedControl()
	self.ledControlInstance.init()


	print("LED TEST...")
	time.sleep(2)
	print("Red...")
	self.ledControlInstance.ledOnRed()
	time.sleep(1)
	print("Green...")
	self.ledControlInstance.ledOnGreen()
	time.sleep(1)
	print("Blue...")
	self.ledControlInstance.ledOnBlue()
	time.sleep(1)	
	self.ledControlInstance.ledOff()
	print("LED TEST END...")

	
	#Initialize Tracking Instance
	global trackingInstance #This lets the object work in another thread
        self.trackingInstance = Tracking() # instance of Tracking from thermaldisplay.py
	self.trackingInstance.init_tracking()

	#Initialize Monkey Control Instance
	global monkeyControlInstance
	self.monkeyControlInstance = MonkeyControl()
	self.monkeyControlInstance.init()

	'''
	print("TEST MONKEY...")
	time.sleep(3)
	self.monkeyControlInstance.monkey_on()
	time.sleep(3)
	self.monkeyControlInstance.monkey_off()
	print("TEST MONKEY END...")
	'''

	
	

	print "threads start..."

        self.t = threading.Thread(group=None,target=self.etsSignedService)
        self.t.start()


        
        self.breakReminderServiceThread = threading.Thread(group=None,target=self.breakReminderService)
        self.breakReminderServiceThread.start()
	
	
	#Set LED to Green
	self.ledControlInstance.ledOnGreen()	
	
	print "GUI Init finished!\n"
	
	
        
       #This method creates the Main Screen on initialization. The Main Screen remains displayed.
    def initCreateMainScreen(self):
	
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)
        
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1,weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(2,weight=1)        
        self.rowconfigure(3, weight=1)
        self.columnconfigure(3,weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(4,weight=1)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(5,weight=1)
        self.rowconfigure(6, weight=1)
        self.columnconfigure(6,weight=1)
        


        
        #Create and hide Manual Indicator Checkbox.
        self.manualIndicatorIntVar = tk.IntVar()
        self.manualIndicatorCheckBox = tk.Checkbutton(self,
                                                      text="Away",
                                                      command=self.eventManualIndicatorCheckBox,
                                                      variable=self.manualIndicatorIntVar)
        self.manualIndicatorCheckBox.grid(row=0,column=4,sticky=tk.N+tk.E+tk.S+tk.W)
        
        #Create and display text label (shows number of minutes input from numpad)
        self.numpadTextStringVar = tk.StringVar()
        self.numpadTextStringVar.set(self.breakTimerInstance.getDisplayString() + " " + "mins")
        self.numpadText = tk.Label(self,text=self.numpadTextStringVar,textvariable=self.numpadTextStringVar)
        self.numpadText.grid(row=0,columnspan=3,sticky=tk.N+tk.E+tk.S+tk.W)

        
        #Create and display Clear and Break Buttons
        self.clearButton = tk.Button(self,text="Clear",foreground="red",background="grey",command=self.clearTextLabel,width=4)
        self.clearButton.grid(row=2,column=4)
        
        self.breakButton = tk.Button(self,
                                     text="Break!",
                                     foreground="green",
                                     background="grey",
                                     command= lambda: threading.Thread(target=self.switchToBreakScreen).start(),width=4)
                                     
        self.breakButton.grid(row=3,column=4)
        
        #Create and display "ETS Signed" Checkbox
        self.etsSignedIntVar = tk.IntVar()
        self.etsSignedCheckBox = tk.Checkbutton(self,
                                                text="ETS Signed",
                                                command=self.eventEtsSignedCheckbox,
                                                variable=self.etsSignedIntVar)
        self.etsSignedCheckBox.grid(row=5,column=4,sticky=tk.N+tk.E+tk.S+tk.W)
        
        #Button to navigate to Settings Page
        self.settingsButton = tk.Button(self,text="Settings",command=self.switchToSettingsGeneralScreen,width=5)
        self.settingsButton.grid(row=5,columnspan=2)

        
        #Create and display Number Pad
        self.numpad = []
        
        kk = 0
        for ii in range(4,0,-1):
            if ii == 4:
                self.aButton = tk.Button(self,text=str(kk),foreground="black",background="grey",command = partial(self.updateTextLabel,kk))
                self.numpad.insert(kk,self.aButton)
                self.numpad[kk].grid(row=ii,column=1,sticky=tk.N+tk.E+tk.S+tk.W)
                kk+=1
            else:
                for jj in range(0,3):
                    self.aButton = tk.Button(self,text=str(kk),foreground="black",background="grey",command = partial(self.updateTextLabel,kk))
                    self.numpad.insert(kk,self.aButton)
                    self.numpad[kk].grid(row=ii,column=jj,sticky=tk.N+tk.E+tk.S+tk.W)
                    kk+=1

        #Set active screen flag
        self.isMainScreenActive = True
        
    #Create the Break Screen on initialization and hide it.
    #This means that on clicking "Break" the application merely hides the Main Screen and displays the Break Screen.
    def initCreateBreakScreen(self):

        self.breakScreen = BreakScreen()
        
        #Cancel Button
        self.breakPageCancelButton = tk.Button(self.breakScreen,text="Cancel",command=self.switchToMainScreen)
        self.breakPageCancelButton.grid(row=1,column=1,sticky=tk.N+tk.E+tk.S+tk.W)
        
        #Message to user
        self.breakPageMessage = tk.Label(self.breakScreen,text="Returns in: {0} Minutes".format("XX"))
        self.breakPageMessage.grid(row=0,column=1,sticky=tk.N+tk.E+tk.S+tk.W)
        
        #hide Break Screen
        self.breakScreen.grid_forget()
        
        
    #Create and hide General Settings Screen
    def initSettingsGeneralScreen(self):
        self.settingsGeneralScreen = SettingsGeneralSceen()
        
        #Create Label Frame to enclose the settings options.
        self.generalSettingsLabelFrame = tk.LabelFrame(self.settingsGeneralScreen,
                                                       text="General Settings")
        self.generalSettingsLabelFrame.grid(row=1)
        
        #Create back button to navigate back to main screen
        self.backButton = tk.Button(self.settingsGeneralScreen,
                                    text="< Back",
                                    command=self.switchToMainScreen)
        self.backButton.grid(row=0,column=0,sticky=tk.W)
        
        #Create forward button that navigates to ETS Reminder Settings Screen
        self.forwardButton = tk.Button(self.settingsGeneralScreen,
                                       text="Next >",
                                       command=self.switchToSettingsETSReminderScreen)
        self.forwardButton.grid(row=0,column=2)
        
        
        #Create Checkbox to deactivate Monkey
        self.deactivateMonkeyIntVar = tk.IntVar()
        self.deactivateMonkeyStringVar = tk.StringVar()
        self.monkeyCheckButton = tk.Checkbutton(self.generalSettingsLabelFrame,
                                                text="Deactivate Monkey",
                                                variable=self.deactivateMonkeyIntVar)
        self.monkeyCheckButton.grid(row=1,columnspan=2,sticky=tk.W)
        
        #Add deactivateMonkeyIntVar to stringVarsDict
        self.deactivateMonkeyStringVar.set(str(self.deactivateMonkeyIntVar.get()))
        self.stringVarsDict[self.breakTimerInstance.getSettingsDeactivateMonkeyKey()] = self.deactivateMonkeyStringVar
        #Create a SAVE button
        self.saveSettingsButton = tk.Button(self.settingsGeneralScreen,text="Save",command=self.doSaveSettings)
        self.saveSettingsButton.grid(row=2,column=2)
        
        
        #Hide screen
        self.settingsGeneralScreen.grid_forget()

        
    #Create and hide ETS Reminder Settings Screen
    def initSettingsETSReminderScreen(self):
  
        self.settingsETSReminderScreen = SettingsETSReminderScreen()
        
        #Create Label Frame to enclose the settings options.
        self.etsReminderLabelFrame = tk.LabelFrame(self.settingsETSReminderScreen,
                                                   text="ETS Reminder Settings")
        self.etsReminderLabelFrame.grid(row=1)
        
        #Create back button to navigate back to General Settings Screen
        self.backButton = tk.Button(self.settingsETSReminderScreen,
                                    text="< Back",
                                    command=self.switchToSettingsGeneralScreen)
        self.backButton.grid(row=0,column=0,sticky=tk.W)
        
        #Create forward button that navigates to next settings screen
        self.forwardButton = tk.Button(self.settingsETSReminderScreen,
                                       text="Next >",
                                       command=self.switchToSettingsBreakReminderScreen)
        self.forwardButton.grid(row=0,column=2)
        
        
        #Create menu for user to select hour
        self.leavingHourStringVar = tk.StringVar()
        self.leavingHourStringVar.set("Hour")
        
        self.leavingHourMB = tk.Menubutton(self.etsReminderLabelFrame,
                                           text = self.leavingHourStringVar,
                                           textvariable=self.leavingHourStringVar,
                                           relief = tk.RAISED,
                                           width=6)
        self.leavingHourMB.grid(row=1, columnspan=2,sticky=tk.W)
        
        #Link menu to menubutton
        self.leavingHourMB.menu = tk.Menu(self.leavingHourMB,tearoff=0)
        self.leavingHourMB["menu"] = self.leavingHourMB.menu

        #Add menu options
        for ii in range(1,13):
            self.leavingHourMB.menu.add_command(label=str(ii),command=partial(self.hourSelectedCommand,ii))

        #Add menu button and stringvar to dictionary
        #Can't call a function to set a key when initializing a dictionary in Python. The "leavingHour" key is intended to match
        #settingsLeavingHourKey in BreakTimer.py
        self.menuButtonsDict = {"leavingHour" : self.leavingHourMB}
        self.stringVarsDict = {"leavingHour" : self.leavingHourStringVar}        

        #Create menu for user to select minute
        self.leavingMinStringVar = tk.StringVar()
        self.leavingMinStringVar.set("Min")
        
        self.leavingMinMB = tk.Menubutton(self.etsReminderLabelFrame,
                                          text = self.leavingMinStringVar,
                                          textvariable=self.leavingMinStringVar,
                                          relief=tk.RAISED,
                                          width=6)
        self.leavingMinMB.grid(row=2,columnspan=2,sticky=tk.W)
        
        #Link menu to menubutton
        self.leavingMinMB.menu = tk.Menu(self.leavingMinMB,tearoff=0)
        self.leavingMinMB["menu"] = self.leavingMinMB.menu
        
        #Add menu options
        self.leavingMinMB.menu.add_command(label="00",command=partial(self.minSelectedCommand,"00"))
        self.leavingMinMB.menu.add_command(label="15",command=partial(self.minSelectedCommand,"15"))
        self.leavingMinMB.menu.add_command(label="30",command=partial(self.minSelectedCommand,"30"))
        self.leavingMinMB.menu.add_command(label="45",command=partial(self.minSelectedCommand,"45"))

        #Add menu button and stringvar to dictionary
        self.menuButtonsDict[self.breakTimerInstance.getSettingsLeavingMinSettingsKey()] = self.leavingMinMB
        self.stringVarsDict[self.breakTimerInstance.getSettingsLeavingMinSettingsKey()] = self.leavingMinStringVar

        #Create menu for user to select period (AM or PM)
        self.leavingPeriodStringVar = tk.StringVar()
        self.leavingPeriodStringVar.set("Period")
        
        self.leavingPeriodMB = tk.Menubutton(self.etsReminderLabelFrame,
                                             text = self.leavingPeriodStringVar,
                                             textvariable=self.leavingPeriodStringVar,
                                             relief=tk.RAISED)
        self.leavingPeriodMB.grid(row=3,columnspan=2,sticky=tk.W)

        #Link menu to menubutton
        self.leavingPeriodMB.menu = tk.Menu(self.leavingPeriodMB,tearoff=0)
        self.leavingPeriodMB["menu"] = self.leavingPeriodMB.menu

        #Add menu options
        self.leavingPeriodMB.menu.add_command(label="AM",command=partial(self.periodSelectedCommand,"AM"))
        self.leavingPeriodMB.menu.add_command(label="PM",command=partial(self.periodSelectedCommand,"PM"))

        #Add menu button and stringvar to dictionary
        self.menuButtonsDict[self.breakTimerInstance.getSettingsLeavingPeriodSettingsKey()] = self.leavingPeriodMB
        self.stringVarsDict[self.breakTimerInstance.getSettingsLeavingPeriodSettingsKey()] = self.leavingPeriodStringVar
        

        #Create menu for user to select configurable amount of minutes to alert user with specified leaving time
        self.timeWithinStringVar = tk.StringVar()
        self.timeWithinStringVar.set("Time Within")
        
        self.timeWithinMB = tk.Menubutton(self.etsReminderLabelFrame,
                                          text=self.timeWithinStringVar,
                                          textvariable=self.timeWithinStringVar,
                                          relief=tk.RAISED)
        self.timeWithinMB.grid(row=4,columnspan=2,sticky=tk.W)
        
        #Link menu to menubutton
        self.timeWithinMB.menu = tk.Menu(self.timeWithinMB,tearoff=0)
        self.timeWithinMB["menu"] = self.timeWithinMB.menu

        #Add menu options
        self.timeWithinMB.menu.add_command(label="15 min",command=partial(self.timeWithinSelectedCommand,"15"))
        self.timeWithinMB.menu.add_command(label="30 min",command=partial(self.timeWithinSelectedCommand,"30"))
        self.timeWithinMB.menu.add_command(label="45 min",command=partial(self.timeWithinSelectedCommand,"45"))
        self.timeWithinMB.menu.add_command(label="60 min",command=partial(self.timeWithinSelectedCommand,"60"))

        #Add menu button and stringvar to dictionary
        self.menuButtonsDict[self.breakTimerInstance.getSettingsTimeWithinSettingsKey()] = self.timeWithinMB
        self.stringVarsDict[self.breakTimerInstance.getSettingsTimeWithinSettingsKey()] = self.timeWithinStringVar



        #Create a SAVE button
        self.saveSettingsButton = tk.Button(self.settingsETSReminderScreen,text="Save",command=self.doSaveSettings)
        self.saveSettingsButton.grid(row=2,column=2)


        #Hide Settings Screen
        self.settingsETSReminderScreen.grid_forget()
        
        
    #Create and hide Break Reminder Settings Screen
    def initSettingsBreakReminderScreen(self):
        self.settingsBreakReminderScreen = SettingsBreakReminderScreen()
        
        #Create Label Frame to enclose the settings options.
        self.breakReminderLabelFrame = tk.LabelFrame(self.settingsBreakReminderScreen,
                                                     text="Break Reminder Settings")
        self.breakReminderLabelFrame.grid(row=1)
        
        #Create back button to navigate back to ETS Reminder Settings Screen
        self.backButton = tk.Button(self.settingsBreakReminderScreen,
                                    text="< Back",
                                    command=self.switchToSettingsETSReminderScreen)
        self.backButton.grid(row=0,column=0,sticky=tk.W)
        
        #Create menu for user to select number of minutes for break reminder
        self.breakReminderMinutesStringVar = tk.StringVar()
        self.breakReminderMinutesStringVar.set("Min")
        
        self.breakReminderMB = tk.Menubutton(self.breakReminderLabelFrame,
                                                text=self.breakReminderMinutesStringVar,
                                                textvariable=self.breakReminderMinutesStringVar,
                                                relief=tk.RAISED,
                                                width=6)
        self.breakReminderMB.grid(row=1,columnspan=2,stick=tk.W)
        
        #Link menu to menubutton
        self.breakReminderMB.menu = tk.Menu(self.breakReminderMB,tearoff=0)
        self.breakReminderMB["menu"] = self.breakReminderMB.menu
        
        #Add menu options
        self.breakReminderMB.menu.add_command(label="15",command=partial(self.breakReminderMinSelectedCommand,"15"))
        self.breakReminderMB.menu.add_command(label="30",command=partial(self.breakReminderMinSelectedCommand,"30"))
        self.breakReminderMB.menu.add_command(label="45",command=partial(self.breakReminderMinSelectedCommand,"45"))
        self.breakReminderMB.menu.add_command(label="60",command=partial(self.breakReminderMinSelectedCommand,"60"))
        
        #Add to menubar and string vars dictionaries
        self.menuButtonsDict[self.breakTimerInstance.getSettingsBreakReminderMinutesKey()] = self.breakReminderMB
        self.stringVarsDict[self.breakTimerInstance.getSettingsBreakReminderMinutesKey()] = self.breakReminderMinutesStringVar

        #Create a SAVE button
        self.saveSettingsButton = tk.Button(self.settingsBreakReminderScreen,text="Save",command=self.doSaveSettings)
        self.saveSettingsButton.grid(row=2,column=2)

        #Hide screen
        self.settingsBreakReminderScreen.grid_forget()
        
    #This function executes when the user selects an hour
    def hourSelectedCommand(self,hourSelected):
        self.leavingHourStringVar.set(str(hourSelected))
        
    #This function executes when the user selects a minute
    def minSelectedCommand(self,minSelected):
        self.leavingMinStringVar.set(minSelected)

    #This function executes when the user selects a period
    def periodSelectedCommand(self,periodSelected):
        self.leavingPeriodStringVar.set(periodSelected)
        
    def timeWithinSelectedCommand(self,timeWithinSelected):
        self.timeWithinStringVar.set(timeWithinSelected)

    def doSaveSettings(self):

        #Refresh menubar text.
        for menuButton in self.menuButtonsDict:
            self.menuButtonsDict[menuButton].update_idletasks()
        
        self.deactivateMonkeyStringVar.set(str(self.deactivateMonkeyIntVar.get()))
        
        #save settings
        self.breakTimerInstance.saveSettings(self.deactivateMonkeyStringVar.get(),
                                             self.leavingHourStringVar.get(),
                                             self.leavingMinStringVar.get(),
                                             self.leavingPeriodStringVar.get(),
                                             self.timeWithinStringVar.get(),
                                             self.breakReminderMinutesStringVar.get())
        
    def breakReminderMinSelectedCommand(self, minSelected):
        self.breakReminderMinutesStringVar.set(minSelected)
        


    #Message displayed on the Break Screen
    def updateBreakScreenMessage(self,returnTime):
        
        if returnTime.hour > 12:
            formattedHour = returnTime.hour - 12
            self.period = "PM"
        else:
            formattedHour = returnTime.hour
            self.period = "AM"
        if returnTime.minute < 10:
            formattedMinute  = "0" + str(returnTime.minute) + " " + self.period
        else:
            formattedMinute = str(returnTime.minute) + " " + self.period

        self.breakPageMessage.config(text="Returns: {0}:{1}  ".format(formattedHour,formattedMinute))
        
        
    def switchToMainScreen(self):
    
        if self.isBreakScreenActive == True:
            
            #End OMRON
            self.breakTimerInstance.endOMRON()
            
            self.breakScreen.grid_forget() #Hide Break Screen
            self.isBreakScreenActive = False
            
            #Start BreakReminderService Thread again
            self.breakReminderServiceThread = threading.Thread(group=None,target=self.breakReminderService)
            self.breakReminderServiceThread.start()
            
        elif self.isSettingsGeneralScreenActive == True:
            self.settingsGeneralScreen.grid_forget() #Hide General Settings Screen
            self.isSettingsGeneralScreenActive = False

        
	
        self.grid() #Display Main Screen
        self.clearTextLabel()
        self.breakLength = 0
        self.isMainScreenActive = True

	#Turn LED to Green
	self.ledControlInstance.ledOnGreen()
    
    #Switch from Main Screen to Break Screen
    def switchToBreakScreen(self):
    
        #Set BreakReminder Flag to end breakReminderService
        self.breakReminderFlag = False
    
        #Update active screen flags
        self.isMainScreenActive     =   False
        self.isBreakScreenActive    =   True
    
        self.grid_forget() #Hide Main Screen
        self.breakScreen.grid() #Display Break Screen
        self.breakLength = int(self.breakTimerInstance.getDisplayString())
        
        clockStart = dt.datetime.now()
        clockExp = clockStart + dt.timedelta(minutes=int(self.breakLength))
        self.updateBreakScreenMessage(clockExp)

	#Set LED to Red
	self.ledControlInstance.ledOnRed()
        
	'''
	# ***NO LONGER VALID??? 2/13/2016***
        #Execute file to run the OMRON sensor. Need to implement logic so that execution ends when user
        #is navigated back to main screen.   
        self.breakTimerInstance.doOMRON
	'''
        
    
    def switchToSettingsGeneralScreen(self):
        if self.isMainScreenActive == True:
            self.grid_forget() #Hide Main Screen
            self.isMainScreenActive = False
        elif self.isSettingsETSScreenActive == True:
            self.settingsETSReminderScreen.grid_forget() #Hide ETS Reminder Settings Screen
            self.isSettingsETSScreenActive = False
            
        self.isSettingsGeneralScreenActive = True
        self.settingsGeneralScreen.grid() #Display General Settings Screen
    
    def switchToSettingsETSReminderScreen(self):
        
        if self.isSettingsGeneralScreenActive == True:
            self.settingsGeneralScreen.grid_forget() #Hide General Settings Screen
            self.isSettingsGeneralScreenActive = False
        elif self.isSettingsBreakReminderScreenActive == True:
            self.settingsBreakReminderScreen.grid_forget() # Hide break reminder settings screen
            self.isSettingsBreakReminderScreenActive = False

        self.isSettingsETSScreenActive  =   True
        self.settingsETSReminderScreen.grid() #Display ETS Reminder Settings Screen

        
    def switchToSettingsBreakReminderScreen(self):
        
        #Update active screen flags
        self.isSettingsETSScreenActive              =   False
        self.isSettingsBreakReminderScreenActive    =   True
        
        self.settingsETSReminderScreen.grid_forget() #Hide ETS Reminder Settings Screen
        self.settingsBreakReminderScreen.grid() #Display Break Reminder Settings Screen
        

    
    def updateTextLabel(self,anInt):
        #Update displayString
        self.breakTimerInstance.updateDisplayString(anInt)
        self.numpadTextStringVar.set(self.breakTimerInstance.getDisplayString() + " " + "mins")
        self.numpadText.update_idletasks()

    def clearTextLabel(self):
        self.breakTimerInstance.clearDisplay()
        self.numpadTextStringVar.set(self.breakTimerInstance.getDisplayString() + " " + "mins")
        self.numpadText.update_idletasks()
    
    def eventManualIndicatorCheckBox(self):
        if self.manualIndicatorIntVar.get() == 1:
            #Away Checkbox is active and need to disable all widgets on main screen and turn LED on.
            self.numpadText.config(state=tk.DISABLED)
            self.clearButton.config(state=tk.DISABLED)
            self.breakButton.config(state=tk.DISABLED)
            self.settingsButton.config(state=tk.DISABLED)
	    self.ledControlInstance.led_on() #LED ON
            for numpadButton in self.numpad:
                numpadButton.config(state=tk.DISABLED)
            
        else:
            #Away Checkbox is not active and all widgets on main screen are enabled and LED is off.
            self.numpadText.config(state=tk.NORMAL)
            self.clearButton.config(state=tk.NORMAL)
            self.breakButton.config(state=tk.NORMAL)
            self.settingsButton.config(state=tk.NORMAL)
            for numpadButton in self.numpad:
                numpadButton.config(state=tk.NORMAL)
            self.ledControlInstance.led_off() #LED OFF
      
      
    def eventEtsSignedCheckbox(self):
        if self.t.isAlive() == False:
            self.t = threading.Thread(group=None,target=self.etsSignedService)
            self.t.start()
      
    
    def etsSignedService(self):
        
	self.etsReminderThreadExit = False	
	timeFormat = "%H:%M:%S %m-%d-%Y"
        
        self.currentMonth = dt.datetime.now().month
        self.currentDay = dt.datetime.now().day
        self.currentYear = dt.datetime.now().year
        
        #Get ETS Reminder Configuration
        self.savedSettings = self.breakTimerInstance.getSavedSettings() #getting latest settings
        if  self.savedSettings[self.breakTimerInstance.getSettingsLeavingPeriodSettingsKey()] == "PM":
            self.leavingHourFormatted =  int(self.savedSettings[self.breakTimerInstance.getSettingsLeavingHourSettingsKey()]) + 12
            self.leavingMinFormatted = self.savedSettings[self.breakTimerInstance.getSettingsLeavingMinSettingsKey()]
            self.leavingTimeFormatted = str(self.leavingHourFormatted)+":"+self.leavingMinFormatted+":"+"00"+" "+str(self.currentMonth)+"-"+str(self.currentDay)+"-"+str(self.currentYear)
        else:
            self.leavingHourFormatted = self.savedSettings[self.breakTimerInstance.getSettingsLeavingHourSettingsKey()]
            self.leavingMinFormatted = self.savedSettings[self.breakTimerInstance.getSettingsLeavingMinSettingsKey()]
            self.leavingTimeFormatted = self.leavingHourFormatted+":"+self.leavingMinFormatted+":"+"00"+" "+str(self.currentMonth)+"-"+str(self.currentDay)+"-"+str(self.currentYear)
        
        #Create datetime object representing the user configured leaving time
        self.leavingTime = dt.datetime.strptime(self.leavingTimeFormatted,timeFormat)
        
        #Trigger time.
        self.timeWithin = self.savedSettings[self.breakTimerInstance.getSettingsTimeWithinSettingsKey()]
        self.timeWithinTimeDelta = dt.timedelta(minutes=int(self.timeWithin))
        self.triggerTime = self.leavingTime - self.timeWithinTimeDelta

        try:
            while self.etsSignedIntVar.get() == 0 and self.allThreadExit == False and self.etsReminderThreadExit == False:
                self.currentTime = dt.datetime.now()
                self.timeDelta = self.triggerTime-self.currentTime
		
                #print current time and trigger time
		'''
                print(" ")
                print("ETS REMINDER SERVICE.....")
                print("Settings Leaving Time: " + self.leavingTimeFormatted)
                print("Settings Time Within: " + str(self.timeWithin))
                print("Current Time: " + str(self.currentTime))
                print("Trigger Time: " + str(self.triggerTime))
                print("Time Delta: " + str(self.timeDelta.days))
                
		'''
		
		print("Presence Detected? " + str(self.trackingInstance.getPresenceInfo()))
		
		if self.trackingInstance.getPresenceInfo() == False:

			print "timeDelta.days: "+str(self.timeDelta.days)			
			
			if self.timeDelta.days < 0:	#after ets limit 
				if self.etsSignedIntVar.get() == 1:
					self.etsReminderThreadExit = True # Terminates the thread.
				else:
					if self.savedSettings[self.breakTimerInstance.getSettingsDeactivateMonkeyKey()] != "1":
						self.monkeyControlInstance.monkey_on()
						#time.sleep(10) #Monkey is On for 10 seconds
						for x in range(0,10):
							self.ledControlInstance.cycleColors()
						self.monkeyControlInstance.monkey_off()
					else:
						for x in range(0,10):
							self.ledControlInstance.cycleColors()
					self.ledControlInstance.ledOnRed()
						

			else:
				self.ledControlInstance.ledOnRed()
				

			
		else:
			self.ledControlInstance.ledOnGreen()
			self.trackingInstance.tracking()
                	time.sleep(.05)
			
			


                



        except:
	    print "Unexpected error:", sys.exc_info()[0]
	    traceback.print_exc()
            self.allThreadExit = True
	    self.ledControlInstance.ledOff()

	print("Turning off motor...")
	self.trackingInstance.turnMotorOff()
	print("Motor off...")
        
        if self.allThreadExit == True:
            print("THREAD TERMINATED...")
        else:
            print("***ETS SERVICE ENDED...***")
        
    def breakReminderService(self):
        #Get Break Reminder Configuration
        self.savedSettings = self.breakTimerInstance.getSavedSettings() #getting latest settings
        if self.savedSettings[self.breakTimerInstance.getSettingsBreakReminderMinutesKey()] == "Min":
            self.breakReminderMinutes = "30"
        else:
            self.breakReminderMinutes = self.savedSettings[self.breakTimerInstance.getSettingsBreakReminderMinutesKey()]
        self.breakReminderTimeDelta = dt.timedelta(minutes=int(self.breakReminderMinutes))
        #self.breakReminderTimeDelta = dt.timedelta(minutes=1) #only for demonstration purposes
        self.breakReminderTriggerTime = dt.datetime.now() + self.breakReminderTimeDelta
        
        self.breakReminderFlag = True
        try:
            while (self.breakReminderFlag and self.allThreadExit == False):
                self.breakReminderCurrentTime = dt.datetime.now()
                self.breakReminderTimeDelta = self.breakReminderTriggerTime - self.breakReminderCurrentTime
                ''''
                #Print Current Time and Trigger Time
                print(" ")
                print("BREAK REMINDER SERVICE.....")
                print("Break Reminder Current Time: " + str(self.breakReminderCurrentTime))
                print("Break Reminder Trigger Time: " + str(self.breakReminderTriggerTime))
                print("Break Reminder Current Time Delta: " + str(self.breakReminderTimeDelta.days))
                '''
                if self.breakReminderTimeDelta.days < 0 and self.isMainScreenActive == True:
                    #Deactivate buttons on main screen
                    self.clearButton.config(state=tk.DISABLED)
                    self.clearButton.update_idletasks()
                    self.breakButton.config(state=tk.DISABLED)
                    self.breakButton.update_idletasks()
                    self.settingsButton.config(state=tk.DISABLED)
                    self.settingsButton.update_idletasks()
                    for numpadButton in self.numpad:
                        numpadButton.config(state=tk.DISABLED)
                        numpadButton.update_idletasks()
                    print("***BREAK REMINDER ALERT***")
                    self.numpadTextStringVar.set("Take a break!")
                    self.numpadText.update_idletasks()


                    for x in range(0,7):
                        self.numpadTextStringVar.set("Now!")
                        self.numpadText.update_idletasks()
                        time.sleep(1)
                        self.numpadTextStringVar.set("Take a break!")
                        self.numpadText.update_idletasks()
                        time.sleep(1)
                    self.numpadTextStringVar.set(self.breakTimerInstance.getDisplayString() + " " + "mins")
                    self.numpadText.update_idletasks()
                    
                    #Activate buttons on main screen
                    self.clearButton.config(state=tk.NORMAL)
                    self.clearButton.update_idletasks
                    self.breakButton.config(state=tk.NORMAL)
                    self.breakButton.update_idletasks()
                    self.settingsButton.config(state=tk.NORMAL)
                    self.settingsButton.update_idletasks()
                    for numpadButton in self.numpad:
                        numpadButton.config(state=tk.NORMAL)
                        numpadButton.update_idletasks()
                    self.breakReminderFlag = False
                #else:
                    #print("***DO NOTHING***")
                #print("BREAK REMINDER SERVICE LOOP END.....")
                
                #Check every 1 second
		time.sleep(10)




        except:
	    print "Unexpected error:", sys.exc_info()[0]
	    traceback.print_exc()
            self.allThreadExit = True
        
        if self.allThreadExit == True:
            print("THREAD TERMINATED...")
             
    
#main program starts here
if __name__ == '__main__':
    
    try:

        app = Application()
        app.master.title('Presence Indicator')
        app.mainloop() #starts application's main loop, waiting for mouse and keyboard events
    except RuntimeError:
        app.threadExit = True
        sys.exit()
        print("I caught an exception")

        
        

