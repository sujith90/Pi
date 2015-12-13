import Tkinter as tk
from BreakTimer import BreakTimer
from _functools import partial
from multiprocessing import Process, Value, Lock
import datetime as dt


class Page(tk.Frame):
    #This Page corresponds to the Break Screen
    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        
        self.grid()
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0,weight=1)


class Application(tk.Frame):
    #This is the main application
    def __init__(self,master=None):
        
        tk.Frame.__init__(self, master)
        
        
        
        self.breakTimerInstance = BreakTimer() # instance of BreakTimer from BreakTimer.py
        self.grid()
        self.initCreateMainScreen()
        self.initCreateBreakScreen()
        
        
        #**These were being used in attempt of multiprocessing. May or may not be needed, but leaving here for now.**
        #self.breakLength = Value('i',int(self.breakTimerInstance.getDisplayString()))
        #self.isTimerDone = Value('i',0)
        #self.lock = Lock()

        
        #This method creates the Main Screen on initialization. The Main Screen remains displayed.
    def initCreateMainScreen(self):

        
        
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0,weight=1)
        

        
        #Create and display Manual Override Checkbox
        self.manualOverrideCheckBox = tk.Checkbutton(self,text="Manual Override",command=self.toggleManualOverrideCheckBox)
        self.manualOverrideCheckBox.grid(row=0,column=4)

        
        
        #Create and hide Manual Indicator Checkbox.
        self.manualIndicatorCheckBox = tk.Checkbutton(self,text="Away",command=self.breakTimerInstance.togglePresenceIndicator)
        self.manualIndicatorCheckBox.grid(row=1,column=4)

        self.manualIndicatorCheckBox.grid_remove()
        
        #Create and display text label (shows number of minutes input from numpad)
        self.textLabel = tk.Label(self,text=self.breakTimerInstance.displayString + " " + "mins")
        self.textLabel.grid(row=0,columnspan=4)

        
        #Create and display Clear and Break Buttons
        self.clearButton = tk.Button(self,text="Clear",foreground="red",background="grey",command=self.clearTextLabel)
        self.clearButton.grid(row=2,column=4)
        
        self.breakButton = tk.Button(self,text="Break!",foreground="green",background="grey",command=self.switchToBreakScreen)
        self.breakButton.grid(row=3,column=4)

        
        #Create and display Number Pad
        self.numpad = []
        
        kk = 0
        for ii in range(4,0,-1):
            
            if ii == 4:
                self.aButton = tk.Button(self,text=str(kk),foreground="black",background="grey",command = partial(self.updateTextLabel,kk))
                self.numpad.insert(kk,self.aButton)
                self.numpad[kk].grid(row=ii,column=1)
                kk+=1
    
            else:
                for jj in range(0,3):
                    self.aButton = tk.Button(self,text=str(kk),foreground="black",background="grey",command = partial(self.updateTextLabel,kk))
                    self.numpad.insert(kk,self.aButton)
                    self.numpad[kk].grid(row=ii,column=jj)
                    kk+=1

        
        #Create and display bottom note
        self.bottomNote = tk.Label(self,text="Note: Max input is 99 mins")
        self.bottomNote.grid(row=6,columnspan=7)

    #Create the Break Screen on initialization and hide it.
    #This means that on clicking "Break" the application merely hides the Main Screen and displays the Break Screen.
    def initCreateBreakScreen(self):

        self.breakScreen = Page()
        
        #Cancel Button
        self.breakPageCancelButton = tk.Button(self.breakScreen,text="Cancel",command=self.switchToMainScreen)
        self.breakPageCancelButton.grid(row=1,column=1)
        
        #Message to user
        self.breakPageMessage = tk.Label(self.breakScreen,text="Returns in: {0} Minutes".format("XX"))
        self.breakPageMessage.grid(row=0,column=1)
        
        #hide Break Screen
        self.breakScreen.grid_forget()
        
    #Message displayed on the Break Screen
    def updateBreakScreenMessage(self,returnTime):
        
        if returnTime.hour > 12:
            formattedHour = returnTime.hour - 12
        else:
            formattedHour = returnTime.hour
        if returnTime.minute < 10:
            formattedMinute  = "0" + str(returnTime.minute)
                
        print(str(formattedMinute))
        
        self.breakPageMessage.config(text="Returns: {0}:{1}  ".format(formattedHour,formattedMinute))
        
    
    #Switch from Main Screen to Break Screen
    def switchToBreakScreen(self):
        self.grid_forget() #Hide Main Screen
        self.breakScreen.grid() #Display Break Screen
        self.breakLength = int(self.breakTimerInstance.getDisplayString())
        
        clockStart = dt.datetime.now()
        clockExp = clockStart + dt.timedelta(minutes=int(self.breakLength))
        self.updateBreakScreenMessage(clockExp)
        
        #print self.breakLength
        #self.p = Process(target=self.breakTimerInstance.startBreak,args=(self.breakLength,self.lock,self.isTimerDone,self.breakPageMessage))
        #self.p.start()
        #self.p1 = Process(target=self.whileUpdateBreak)
        #self.p1.start()
        #self.breakTimerInstance.startBreak(self.breakLength,self.lock,self.isTimerDone,self,self.breakScreen)

        
        
        
    
    def switchToMainScreen(self):
        self.breakScreen.grid_forget() #Hide Break Screen
        self.grid() #Display Main Screen
        self.clearTextLabel()
        self.breakLength = 0
        
        
    
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
        
        
