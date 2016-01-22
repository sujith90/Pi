import datetime as dt
from math import ceil
import time
import os.path
import json

class BreakTimer():

    def __init__(self):
        self.displayString              = "0"
        self.manualPresenceIndicator    = False
        self.isTimeExpired              = False
        self.textLengthErrorFlag        = False
        self.isSettingsDefault          = True
        self.returnTime                 = 0 #mins
        
        #Settings Keys
        self.settingsLeavingHourKey      = "leavingHour"
        self.settingsLeavingMinKey       = "leavingMin"
        self.settingsLeavingPeriodKey    = "leavingPeriod"
        self.settingsTimeWithinKey       = "timeWithin"
        
        #Settings Default Values
        self.settingsLeavingHourDefault     = "5"
        self.settingsLeavingMinDefault      = "00"
        self.settingsLeavingPeriodDefault   = "PM"
        self.settingsTimeWithinDefault      = "15"
        
        #Create dictionary for default settings
        self.defaultSettings = { self.settingsLeavingHourKey     : self.settingsLeavingHourDefault,
                                 self.settingsLeavingMinKey      : self.settingsLeavingMinDefault,
                                 self.settingsLeavingPeriodKey   : self.settingsLeavingPeriodDefault,
                                 self.settingsTimeWithinKey      : self.settingsTimeWithinDefault
            
            
        } 
        
    def loadSettings(self):  
        
        #Load settings from settings.json. If the file does not exist, create settings.json.
        if (os.path.exists("/Users/noebrito/OneDrive/Github_Pi/GUI/settings.json")): #change path when run on Pi
            with open("settings.json",'r') as settingsFile:
                self.savedSettings = json.loads(settingsFile.readline())
                if self.savedSettings != self.defaultSettings:
                    self.isSettingsDefault = False
        else: #Creates settings.json and loads with default settings
            with open("settings.json",'w') as settingsFile:
                settingsFile.write(json.dumps(self.defaultSettings)) #Python Dictionary --> JSON Object

    #Clear's the display text
    def clearDisplay(self):
        self.displayString = "0"
        
        
    #Logic to update display text
    def updateDisplayString(self,anInt):
        if self.displayString == "0":
            self.displayString = str(anInt)
        else:
            if len(self.displayString) < 3: #999 is max number of minutes
                self.displayString += str(anInt)
                
        
    
    def togglePresenceIndicator(self):
        if self.manualPresenceIndicator == True:
            self.manualPresenceIndicator = False
        else:
            self.manualPresenceIndicator = True

    
    def getReturnTime(self):
        return self.returnTime
    
    def getDisplayString(self):
        return self.displayString
    
    def getManualOverrideCheck(self):
        return self.manualOverrideFlag
    
    def getManualPresenceIndicator(self):
        return self.manualPresenceIndicator
    
    def getTextLengthError(self):
        return self.textLengthErrorFlag
        
    def getIsSettingsDefault(self):
        return self.isSettingsDefault
        
        
        
    #Get Settings Keys
    def getLeavingHourSettingsKey(self):
        return self.settingsLeavingHourKey
    
    def getLeavingMinSettingsKey(self):
        return self.settingsLeavingMinKey
    
    def getLeavingPeriodSettingsKey(self):
        return self.settingsLeavingPeriodKey
    
    def getTimeWithinSettingsKey(self):
        return self.settingsTimeWithinKey
    
    def getSavedSettings(self):
        return self.savedSettings
        
    def getDefaultSettings(self):
        return self.defaultSettings
    
    
    def saveSettings(self,leavingHour,leavingMin,leavingPeriod,timeWithin):
        
        if leavingHour == "Hour":
            leavingHour = self.settingsLeavingHourDefault
        if leavingMin == "Min":
            leavingMin = self.settingsLeavingMinDefault
        if leavingPeriod == "Period":
            leavingPeriod = self.settingsLeavingPeriodDefault
        if timeWithin == "Time Within":
            timeWithin = self.settingsTimeWithinDefault
        
        
        #create dictionary with settings that are to be saved.
        self.savedSettings = { self.settingsLeavingHourKey     : leavingHour,
                               self.settingsLeavingMinKey      : leavingMin,
                               self.settingsLeavingPeriodKey   : leavingPeriod,
                               self.settingsTimeWithinKey      : timeWithin
        }
        
        
        #Write the new settings to settings.json
        with open("settings.json",'w') as settingsFile:
            
            settingsFile.write(json.dumps(self.savedSettings))

    #Execute file that activates OMRON sensor
    def doOMRON(self):
        print("***Doing OMRON***")

        #execfile("/Users/noebrito/OneDrive/Github_Pi/Omron/thermal-display.py")
        
    def activateLED(self):
        print("Turn LED ON")
    
    def deactivateLED(self):
        print("Turn LED OFF")
    

    
        
