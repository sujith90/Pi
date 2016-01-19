import datetime as dt
from math import ceil
import time
import os.path
import json

class BreakTimer():

    def __init__(self):
        self.displayString              = "0"
        self.manualOverrideFlag         = False
        self.manualPresenceIndicator    = False
        self.isTimeExpired              = False
        self.textLengthErrorFlag        = False
        self.isSettingsDefault          = True
        self.returnTime                 = 0 #mins
        
        #Settings Keys
        self.settingsReturnHourKey      = "returnHour"
        self.settingsReturnMinKey       = "returnMin"
        self.settingsReturnPeriodKey    = "returnPeriod"
        self.settingsTimeWithinKey      = "timeWithin"
        
        #Settings Default Values
        self.settingsReturnHourDefault  = "5"
        self.settingsReturnMinDefault   = "00"
        self.settingsPeriodDefault      = "PM"
        self.settingsTimeWithinDefault  = "15"
        
        #Create dictionary for default settings
        self.defaultSettings = { self.settingsReturnHourKey     : self.settingsReturnHourDefault,
                                 self.settingsReturnMinKey      : self.settingsReturnMinDefault,
                                 self.settingsReturnPeriodKey   : self.settingsPeriodDefault,
                                 self.settingsTimeWithinKey     : self.settingsTimeWithinDefault
            
            
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
        self.textLengthErrorFlag = False
        self.displayString = "0"
        self.inputDisplayString = "0"
        
        
    #Logic to update display text
    def updateDisplayString(self,anInt):
        if self.displayString == "0":
            self.displayString = str(anInt)
        else:
            if len(self.displayString) < 3: #999 is max number of minutes
                self.displayString += str(anInt)
            else:
                self.textLengthError = True
                
    
    def toggleManualOverrideFlag(self):
        if self.manualOverrideFlag == False:
            self.manualOverrideFlag = True
        else:
            self.manualOverrideFlag = False
        
    
    def togglePresenceIndicator(self):
        #Only set if manualOverrideFlag is True
        if self.manualOverrideFlag == True:
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
    def getReturnHourSettingsKey(self):
        return self.settingsReturnHourKey
    
    def getReturnMinSettingsKey(self):
        return self.settingsReturnMinKey
    
    def getReturnPeriodSettingsKey(self):
        return self.settingsReturnPeriodKey
    
    def getTimeWithinSettingsKey(self):
        return self.settingsTimeWithinKey
    
    
    def getSavedSettings(self):
        return self.savedSettings    
    
    
    def saveSettings(self,returnHour,returnMin,returnPeriod,timeWithin):
        
        #create dictionary with settings that are to be saved.
        self.savedSettings = { self.settingsReturnHourKey       : returnHour,
                                 self.settingsReturnMinKey      : returnMin,
                                 self.settingsReturnPeriodKey   : returnPeriod,
                                 self.settingsTimeWithinKey     : timeWithin
        }
        
        
        #Write the new settings to settings.json
        with open("settings.json",'w') as settingsFile:
            
            settingsFile.write(json.dumps(self.savedSettings))

    #Execute file that activates OMRON sensor
    def doOMRON(self):
        print("***Doing OMRON***")

        #execfile("/Users/noebrito/OneDrive/Github_Pi/Omron/thermal-display.py")
        
    
    #**STUB METHOD**
    def toggleLED(self):
        print "Toggle LED"
    

    
        
