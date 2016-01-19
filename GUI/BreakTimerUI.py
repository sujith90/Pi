import Tkinter as tk
from BreakTimer import BreakTimer
from _functools import partial
import threading
import datetime as dt





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
        
        self.grid()
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)

        


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
            print("DEBUG: Settings are not default!")
            self.savedSettings = self.breakTimerInstance.getSavedSettings()
            index = 0
            for each in self.stringVarsDict:
                print(each)
                self.stringVarsDict[each].set(self.savedSettings[each])
                index+=1
        else:
            print("DEBUG: Settings are default.")
                

        
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
        

        
        #Create and display Manual Override Checkbox
        self.manualOverrideCheckBox = tk.Checkbutton(self,text="Manual Override",command=self.toggleManualOverrideCheckBox)
        self.manualOverrideCheckBox.grid(row=0,column=4,sticky=tk.N+tk.E+tk.S+tk.W)

        
        
        #Create and hide Manual Indicator Checkbox.
        self.manualIndicatorCheckBox = tk.Checkbutton(self,text="Away",command=self.breakTimerInstance.togglePresenceIndicator)
        self.manualIndicatorCheckBox.grid(row=1,column=4,sticky=tk.N+tk.E+tk.S+tk.W)

        self.manualIndicatorCheckBox.grid_remove()
        
        #Create and display text label (shows number of minutes input from numpad)
        self.textLabel = tk.Label(self,text=self.breakTimerInstance.displayString + " " + "mins")
        self.textLabel.grid(row=0,columnspan=4,sticky=tk.N+tk.E+tk.S+tk.W)

        
        #Create and display Clear and Break Buttons
        self.clearButton = tk.Button(self,text="Clear",foreground="red",background="grey",command=self.clearTextLabel)
        self.clearButton.grid(row=2,column=4,sticky=tk.N+tk.E+tk.S+tk.W)
        
        self.breakButton = tk.Button(self,text="Break!",foreground="green",background="grey",command= lambda: threading.Thread(target=self.switchToBreakScreen).start())
        self.breakButton.grid(row=3,column=4,sticky=tk.N+tk.E+tk.S+tk.W)
        
        #Button to navigate to Settings Page
        self.settingsButton = tk.Button(self,text="Settings",command=self.switchToSettingsScreen)
        self.settingsButton.grid(row=5,column=4,sticky=tk.N+tk.E+tk.S+tk.W)

        
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

        
        #Create and display bottom note
        self.bottomNote = tk.Label(self,text="Note: Max input is 999 mins")
        self.bottomNote.grid(row=6,columnspan=7,sticky=tk.N+tk.E+tk.S+tk.W)

    #Create the Break Screen on initialization and hide it.
    #This means that on clicking "Break" the application merely hides the Main Screen and displays the Break Screen.
    def initCreateBreakScreen(self):

        self.breakScreen = BreakPage()
        
        #Cancel Button
        self.breakPageCancelButton = tk.Button(self.breakScreen,text="Cancel",command=self.switchToMainScreen)
        self.breakPageCancelButton.grid(row=1,column=1)
        
        #Message to user
        self.breakPageMessage = tk.Label(self.breakScreen,text="Returns in: {0} Minutes".format("XX"))
        self.breakPageMessage.grid(row=0,column=1)
        
        #hide Break Screen
        self.breakScreen.grid_forget()

        
        
    def initSettingsScreen(self):
    
        self.settingsScreen = SettingsPage()
        
        #Create back button to navigate back to main screen
        self.settingsPageBackButton = tk.Button(self.settingsScreen,text="Back",command = self.settingsSwitchToMainScreen)
        self.settingsPageBackButton.grid(row=0,column=0)
        
        
        #Create menu for user to select hour
        self.leavingHourStringVar = tk.StringVar()
        self.leavingHourStringVar.set("Hours")
        
        self.leavingHourMB = tk.Menubutton(self.settingsScreen,text = self.leavingHourStringVar,textvariable=self.leavingHourStringVar, relief = tk.RAISED)
        self.leavingHourMB.grid(row=1, column=0)
        
        self.leavingHourMB.menu = tk.Menu(self.leavingHourMB,tearoff=0)
        self.leavingHourMB["menu"] = self.leavingHourMB.menu
        
        for ii in range(1,13):
            self.leavingHourMB.menu.add_command(label=str(ii),command=partial(self.hourSelectedCommand,ii))

        #Add menu button and stringvar to dictionary
        #Can't call a function to set a key when initializing a dictionary in Python. The "returnHour" key is intended to match
        #settingsReturnHourKey in BreakTimer.py
        self.menuButtonsDict = {"returnHour" : self.leavingHourMB}
        self.stringVarsDict = {"returnHour" : self.leavingHourStringVar}        

        #Create menu for user to select minute
        self.leavingMinStringVar = tk.StringVar()
        self.leavingMinStringVar.set("Mins")
        
        self.leavingMinMB = tk.Menubutton(self.settingsScreen,text = self.leavingMinStringVar,textvariable=self.leavingMinStringVar,relief=tk.RAISED)
        self.leavingMinMB.grid(row=1,column=1)
        
        self.leavingMinMB.menu = tk.Menu(self.leavingMinMB,tearoff=0)
        self.leavingMinMB["menu"] = self.leavingMinMB.menu

        self.leavingMinMB.menu.add_command(label="00",command=partial(self.minSelectedCommand,"00"))
        self.leavingMinMB.menu.add_command(label="30",command=partial(self.minSelectedCommand,"30"))

        #Add menu button and stringvar to dictionary
        self.menuButtonsDict[self.breakTimerInstance.getReturnMinSettingsKey()] = self.leavingMinMB
        self.stringVarsDict[self.breakTimerInstance.getReturnMinSettingsKey()] = self.leavingMinStringVar

        #Create menu for user to select period (AM or PM)
        self.leavingPeriodStringVar = tk.StringVar()
        self.leavingPeriodStringVar.set("Period")
        
        self.leavingPeriodMB = tk.Menubutton(self.settingsScreen,text = self.leavingPeriodStringVar,textvariable=self.leavingPeriodStringVar,relief=tk.RAISED)
        self.leavingPeriodMB.grid(row=1,column = 2)
        
        self.leavingPeriodMB.menu = tk.Menu(self.leavingPeriodMB,tearoff=0)
        self.leavingPeriodMB["menu"] = self.leavingPeriodMB.menu

        self.leavingPeriodMB.menu.add_command(label="AM",command=partial(self.periodSelectedCommand,"AM"))
        self.leavingPeriodMB.menu.add_command(label="PM",command=partial(self.periodSelectedCommand,"PM"))

        #Add menu button and stringvar to dictionary
        self.menuButtonsDict[self.breakTimerInstance.getReturnPeriodSettingsKey()] = self.leavingPeriodMB
        self.stringVarsDict[self.breakTimerInstance.getReturnPeriodSettingsKey()] = self.leavingPeriodStringVar
        

        #Create menu for user to select configurable amount of minutes to alert user with specified leaving time
        self.timeWithinStringVar = tk.StringVar()
        self.timeWithinStringVar.set("Time Within")
        
        self.timeWithinMB = tk.Menubutton(self.settingsScreen,text=self.timeWithinStringVar,textvariable=self.timeWithinStringVar,relief=tk.RAISED)
        self.timeWithinMB.grid(row=2,column=0)
        
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
        #update everything
        for menuButton in self.menuButtonsDict:
            print(menuButton)
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
        else:
            formattedHour = returnTime.hour
        if returnTime.minute < 10:
            formattedMinute  = "0" + str(returnTime.minute)
        else:
            formattedMinute = str(returnTime.minute)
                
        
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
        
        #refresh textLabel
        self.textLabel.config(text=self.breakTimerInstance.getDisplayString() + " " + "mins")
    

    def clearTextLabel(self):
        self.breakTimerInstance.clearDisplay()
        self.textLabel.config(text=self.breakTimerInstance.getDisplayString() + " " + "mins")
    
    def toggleManualOverrideCheckBox(self):
        self.breakTimerInstance.toggleManualOverrideFlag()
        self.displayManualIndicatorCheckBox()
        
    #the Manual Indicator Checkbox will only display on the GUI only if the Manual Override Checbox is True
    def displayManualIndicatorCheckBox(self):
        if self.breakTimerInstance.getManualOverrideCheck() == True:
            self.manualIndicatorCheckBox.grid()
        else:
            self.manualIndicatorCheckBox.grid_remove()
    
#main program starts here

if __name__ == '__main__':
    app = Application()
    app.master.title('Presence Indicator')
    app.mainloop() #starts application's main loop, waiting for mouse and keyboard events
        
        
