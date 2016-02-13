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
        self.settingsDeactivateMonkeyKey        = "deactivateMonkeyFlag"
        self.settingsLeavingHourKey             = "leavingHour"
        self.settingsLeavingMinKey              = "leavingMin"
        self.settingsLeavingPeriodKey           = "leavingPeriod"
        self.settingsTimeWithinKey              = "timeWithin"
        self.settingsBreakReminderMinutesKey    = "breakReminderMinutes"
        
        #Settings Default Values
        self.settingsDeactivateMonkeyDefault         = "0"
        self.settingsLeavingHourDefault              = "5"
        self.settingsLeavingMinDefault               = "00"
        self.settingsLeavingPeriodDefault            = "PM"
        self.settingsTimeWithinDefault               = "15"
        self.settingsBreakReminderMinutesDefault     = "30"
        
        #Create dictionary for default settings
        self.defaultSettings = { self.settingsDeactivateMonkeyKey       :   self.settingsDeactivateMonkeyDefault,
                                 self.settingsLeavingHourKey            :   self.settingsLeavingHourDefault,
                                 self.settingsLeavingMinKey             :   self.settingsLeavingMinDefault,
                                 self.settingsLeavingPeriodKey          :   self.settingsLeavingPeriodDefault,
                                 self.settingsTimeWithinKey             :   self.settingsTimeWithinDefault,
                                 self.settingsBreakReminderMinutesKey   :   self.settingsBreakReminderMinutesDefault
        } 
        
    def loadSettings(self):  
        
        #Load settings from settings.json. If the file does not exist, create settings.json.
        if (os.path.exists("/home/pi/pi/GUI/settings.json")): #change path when run on Pi
            with open("settings.json",'r') as settingsFile:
                self.savedSettings = json.loads(settingsFile.readline())
                if self.savedSettings != self.defaultSettings:
                    self.isSettingsDefault = False
        else: #Creates settings.json and loads with default settings
            with open("settings.json",'w') as settingsFile:
                settingsFile.write(json.dumps(self.defaultSettings)) #Python Dictionary --> JSON Object
                self.savedSettings = self.defaultSettings

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
        
    def getIsSettingsDefault(self):
        return self.isSettingsDefault
        
        
        
    #Get Settings Keys
    def getSettingsDeactivateMonkeyKey(self):
        return self.settingsDeactivateMonkeyKey
    
    def getSettingsLeavingHourSettingsKey(self):
        return self.settingsLeavingHourKey
    
    def getSettingsLeavingMinSettingsKey(self):
        return self.settingsLeavingMinKey
    
    def getSettingsLeavingPeriodSettingsKey(self):
        return self.settingsLeavingPeriodKey
    
    def getSettingsTimeWithinSettingsKey(self):
        return self.settingsTimeWithinKey
        
    def getSettingsBreakReminderMinutesKey(self):
        return self.settingsBreakReminderMinutesKey
    
    def getSavedSettings(self):
        return self.savedSettings
        
    def getDefaultSettings(self):
        return self.defaultSettings
    
    
    def saveSettings(self,deactivateMonkeyFlag,leavingHour,leavingMin,leavingPeriod,timeWithin,breakReminderMinutes):
        
        #Check if settings are default
        if deactivateMonkeyFlag == "0":
            deactivateMonkeyFlag = self.settingsDeactivateMonkeyDefault
        if leavingHour == "Hour":
            leavingHour = self.settingsLeavingHourDefault
        if leavingMin == "Min":
            leavingMin = self.settingsLeavingMinDefault
        if leavingPeriod == "Period":
            leavingPeriod = self.settingsLeavingPeriodDefault
        if timeWithin == "Time Within":
            timeWithin = self.settingsTimeWithinDefault
        if breakReminderMinutes == "30":
            breakReminderMinutes = self.settingsBreakReminderMinutesDefault
        
        
        #create dictionary with settings that are to be saved.
        self.savedSettings = { self.settingsDeactivateMonkeyKey         :   deactivateMonkeyFlag,
                               self.settingsLeavingHourKey              :   leavingHour,
                               self.settingsLeavingMinKey               :   leavingMin,
                               self.settingsLeavingPeriodKey            :   leavingPeriod,
                               self.settingsTimeWithinKey               :   timeWithin,
                               self.settingsBreakReminderMinutesKey     :   breakReminderMinutes
        }
        
        
        #Write the new settings to settings.json
        with open("settings.json",'w') as settingsFile:
            
            settingsFile.write(json.dumps(self.savedSettings))

    #Execute file that activates OMRON sensor
    def doOMRON(self):
        print("***Doing OMRON***")

        #execfile("/Users/noebrito/OneDrive/Github_Pi/Omron/thermal-display.py")
        
    def endOMRON(self):
        print("***END OMRON***")
        
    def activateLED(self):
        print("Turn LED ON")
    
    def deactivateLED(self):
        print("Turn LED OFF")
    

    
        

