import Tkinter as tk
from BreakTimer import BreakTimer
from _functools import partial
import threading
import datetime as dt
import time





class BreakPage(tk.Frame):
    #This Page corresponds to the Break Screen
    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        
        self.grid()
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)

class SettingsPage(tk.Frame):
    #This page corresponds to the Settings Screen
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


class Application(tk.Frame):
    #This is the main application
    def __init__(self,master=None):
        
        #Creates Main Frame
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W) #Create main Grid of the application
        
        global breakTimerInstance #This lets the object work in another thread
        self.breakTimerInstance = BreakTimer() # instance of BreakTimer from BreakTimer.py
        
        #Create the screens
        self.initCreateMainScreen()
        self.initCreateBreakScreen()
        self.initSettingsScreen()
        
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
            
        self.t = threading.Thread(group=None,target=self.etsSignedService)
        self.t.start()
                

        
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
        self.settingsButton = tk.Button(self,text="Settings",command=self.switchToSettingsScreen,width=5)
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

        
    #Create the Break Screen on initialization and hide it.
    #This means that on clicking "Break" the application merely hides the Main Screen and displays the Break Screen.
    def initCreateBreakScreen(self):

        self.breakScreen = BreakPage()
        
        #Cancel Button
        self.breakPageCancelButton = tk.Button(self.breakScreen,text="Cancel",command=self.switchToMainScreen)
        self.breakPageCancelButton.grid(row=1,column=1,sticky=tk.N+tk.E+tk.S+tk.W)
        
        #Message to user
        self.breakPageMessage = tk.Label(self.breakScreen,text="Returns in: {0} Minutes".format("XX"))
        self.breakPageMessage.grid(row=0,column=1,sticky=tk.N+tk.E+tk.S+tk.W)
        
        #hide Break Screen
        self.breakScreen.grid_forget()

        
        
    def initSettingsScreen(self):
    
        self.settingsScreen = SettingsPage()
        
        self.settingsLabelFrame = tk.LabelFrame(self.settingsScreen,text="ETS Reminder")
        self.settingsLabelFrame.grid(row=1)
        
        #Create back button to navigate back to main screen
        self.settingsPageBackButton = tk.Button(self.settingsScreen,
                                                text="< Back",
                                                command = self.settingsSwitchToMainScreen)
        self.settingsPageBackButton.grid(row=0,column=0,sticky=tk.W)
        
        
        #Create menu for user to select hour
        self.leavingHourStringVar = tk.StringVar()
        self.leavingHourStringVar.set("Hour")
        
        self.leavingHourMB = tk.Menubutton(self.settingsLabelFrame,
                                           text = self.leavingHourStringVar,
                                           textvariable=self.leavingHourStringVar,
                                           relief = tk.RAISED,
                                           width=6)
        self.leavingHourMB.grid(row=1, columnspan=2,sticky=tk.W)
        
        self.leavingHourMB.menu = tk.Menu(self.leavingHourMB,tearoff=0)
        self.leavingHourMB["menu"] = self.leavingHourMB.menu
        
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
        
        self.leavingMinMB = tk.Menubutton(self.settingsLabelFrame,
                                          text = self.leavingMinStringVar,
                                          textvariable=self.leavingMinStringVar,
                                          relief=tk.RAISED,
                                          width=6)
        self.leavingMinMB.grid(row=2,columnspan=2,sticky=tk.W)
        
        self.leavingMinMB.menu = tk.Menu(self.leavingMinMB,tearoff=0)
        self.leavingMinMB["menu"] = self.leavingMinMB.menu

        self.leavingMinMB.menu.add_command(label="00",command=partial(self.minSelectedCommand,"00"))
        self.leavingMinMB.menu.add_command(label="15",command=partial(self.minSelectedCommand,"15"))
        self.leavingMinMB.menu.add_command(label="30",command=partial(self.minSelectedCommand,"30"))
        self.leavingMinMB.menu.add_command(label="45",command=partial(self.minSelectedCommand,"45"))

        #Add menu button and stringvar to dictionary
        self.menuButtonsDict[self.breakTimerInstance.getLeavingMinSettingsKey()] = self.leavingMinMB
        self.stringVarsDict[self.breakTimerInstance.getLeavingMinSettingsKey()] = self.leavingMinStringVar

        #Create menu for user to select period (AM or PM)
        self.leavingPeriodStringVar = tk.StringVar()
        self.leavingPeriodStringVar.set("Period")
        
        self.leavingPeriodMB = tk.Menubutton(self.settingsLabelFrame,
                                             text = self.leavingPeriodStringVar,
                                             textvariable=self.leavingPeriodStringVar,
                                             relief=tk.RAISED)
        self.leavingPeriodMB.grid(row=3,columnspan=2,sticky=tk.W)
        
        self.leavingPeriodMB.menu = tk.Menu(self.leavingPeriodMB,tearoff=0)
        self.leavingPeriodMB["menu"] = self.leavingPeriodMB.menu

        self.leavingPeriodMB.menu.add_command(label="AM",command=partial(self.periodSelectedCommand,"AM"))
        self.leavingPeriodMB.menu.add_command(label="PM",command=partial(self.periodSelectedCommand,"PM"))

        #Add menu button and stringvar to dictionary
        self.menuButtonsDict[self.breakTimerInstance.getLeavingPeriodSettingsKey()] = self.leavingPeriodMB
        self.stringVarsDict[self.breakTimerInstance.getLeavingPeriodSettingsKey()] = self.leavingPeriodStringVar
        

        #Create menu for user to select configurable amount of minutes to alert user with specified leaving time
        self.timeWithinStringVar = tk.StringVar()
        self.timeWithinStringVar.set("Time Within")
        
        self.timeWithinMB = tk.Menubutton(self.settingsLabelFrame,
                                          text=self.timeWithinStringVar,
                                          textvariable=self.timeWithinStringVar,
                                          relief=tk.RAISED)
        self.timeWithinMB.grid(row=4,columnspan=2,sticky=tk.W)
        
        self.timeWithinMB.menu = tk.Menu(self.timeWithinMB,tearoff=0)
        self.timeWithinMB["menu"] = self.timeWithinMB.menu
        
        self.timeWithinMB.menu.add_command(label="15 min",command=partial(self.timeWithinSelectedCommand,"15"))
        self.timeWithinMB.menu.add_command(label="30 min",command=partial(self.timeWithinSelectedCommand,"30"))
        self.timeWithinMB.menu.add_command(label="45 min",command=partial(self.timeWithinSelectedCommand,"45"))
        self.timeWithinMB.menu.add_command(label="60 min",command=partial(self.timeWithinSelectedCommand,"60"))

        #Add menu button and stringvar to dictionary
        self.menuButtonsDict[self.breakTimerInstance.getTimeWithinSettingsKey()] = self.timeWithinMB
        self.stringVarsDict[self.breakTimerInstance.getTimeWithinSettingsKey()] = self.timeWithinStringVar



        #Create a SAVE button
        self.saveSettingsButton = tk.Button(self.settingsScreen,text="Save",command=self.doSaveSettings)
        self.saveSettingsButton.grid(row=2,column=2)


        #Hide Settings Screen
        self.settingsScreen.grid_forget()
        
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
        
        #save settings
        self.breakTimerInstance.saveSettings(self.leavingHourStringVar.get(),
                                             self.leavingMinStringVar.get(),
                                             self.leavingPeriodStringVar.get(),
                                             self.timeWithinStringVar.get())
        



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
        
        
    def settingsSwitchToMainScreen(self):
        self.settingsScreen.grid_forget() #Hide Settings Screen
        self.grid() #Display Main Screen
        self.clearTextLabel()
        self.breakLength = 0
    
    #Switch from Main Screen to Break Screen
    def switchToBreakScreen(self):
        self.grid_forget() #Hide Main Screen
        self.breakScreen.grid() #Display Break Screen
        self.breakLength = int(self.breakTimerInstance.getDisplayString())
        
        clockStart = dt.datetime.now()
        clockExp = clockStart + dt.timedelta(minutes=int(self.breakLength))
        self.updateBreakScreenMessage(clockExp)
        
        #Execute file to run the OMRON sensor. Need to implement logic so that execution ends when user
        #is navigated back to main screen.   
        self.breakTimerInstance.doOMRON()
    
    def switchToMainScreen(self):
        self.breakScreen.grid_forget() #Hide Break Screen
        self.grid() #Display Main Screen
        self.clearTextLabel()
        self.breakLength = 0
        
    def switchToSettingsScreen(self):
        self.grid_forget() #Hide Main Screen
        self.settingsScreen.grid() #Display Settings Screen

    
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
            for numpadButton in self.numpad:
                numpadButton.config(state=tk.DISABLED)
            self.breakTimerInstance.activateLED()
            
        else:
            #Away Checkbox is not active and all widgets on main screen are enabled and LED is off.
            self.numpadText.config(state=tk.NORMAL)
            self.clearButton.config(state=tk.NORMAL)
            self.breakButton.config(state=tk.NORMAL)
            self.settingsButton.config(state=tk.NORMAL)
            for numpadButton in self.numpad:
                numpadButton.config(state=tk.NORMAL)
            self.breakTimerInstance.deactivateLED()
      
      
    def eventEtsSignedCheckbox(self):
        if self.t.isAlive() == False:
            self.t = threading.Thread(group=None,target=self.etsSignedService)
            self.t.start()
      
    
    def etsSignedService(self):
        timeFormat = "%H:%M:%S %m-%d-%Y"
        
        self.currentMonth = dt.datetime.now().month
        self.currentDay = dt.datetime.now().day
        self.currentYear = dt.datetime.now().year
        
        #Get leave time from settings.
        if  self.savedSettings[self.breakTimerInstance.getLeavingPeriodSettingsKey()] == "PM":
            self.leavingHourFormatted =  int(self.savedSettings[self.breakTimerInstance.getLeavingHourSettingsKey()]) + 12
            self.leavingMinFormatted = self.savedSettings[self.breakTimerInstance.getLeavingMinSettingsKey()]
            self.leavingTimeFormatted = str(self.leavingHourFormatted)+":"+self.leavingMinFormatted+":"+"00"+" "+str(self.currentMonth)+"-"+str(self.currentDay)+"-"+str(self.currentYear)
        else:
            self.leavingHourFormatted = self.savedSettings[self.breakTimerInstance.getLeavingHourSettingsKey()]
            self.leavingMinFormatted = self.savedSettings[self.breakTimerInstance.getLeavingMinSettingsKey()]
            self.leavingTimeFormatted = self.leavingHourFormatted+":"+self.leavingMinFormatted+":"+"00"+" "+str(self.currentMonth)+"-"+str(self.currentDay)+"-"+str(self.currentYear)
        
        #Create datetime object representing the user configured leaving time
        self.leavingTime = dt.datetime.strptime(self.leavingTimeFormatted,timeFormat)
        
        #Trigger time.
        self.timeWithin = self.savedSettings[self.breakTimerInstance.getTimeWithinSettingsKey()]
        self.timeWithinTimeDelta = dt.timedelta(minutes=int(self.timeWithin))
        self.triggerTime = self.leavingTime - self.timeWithinTimeDelta

        while self.etsSignedIntVar.get() == 0:
            self.currentTime = dt.datetime.now()
            self.timeDelta = self.triggerTime-self.currentTime

            #print current time and trigger time
            print("Settings Leaving Time: " + self.leavingTimeFormatted)
            print("Settings Time Within: " + str(self.timeWithin))
            print("Current Time: " + str(self.currentTime))
            print("Trigger Time: " + str(self.triggerTime))
            print(" ")
            
            if self.timeDelta.days < 0:
                print("***Activate monkey if presence not detected***")
            else:
                print("***Do not activate monkey if presence is not detected***")
            print(" ")
            
            #Check every 15 seconds
            time.sleep(15)
        
        print("***ETS SIGNED***")
        
        
    
#main program starts here
if __name__ == '__main__':
    app = Application()
    app.master.title('Presence Indicator')
    app.mainloop() #starts application's main loop, waiting for mouse and keyboard events
        
        
