import datetime as dt
from math import ceil
import time

class BreakTimer():

    def __init__(self):
        self.displayString = "0"
        self.manualOverrideFlag = False
        self.manualPresenceIndicator = False
        self.isTimeExpired = False
        self.textLengthErrorFlag = False
        self.returnTime = 0 #mins
        
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
    
    
    #Execute file that activates OMRON sensor
    def doOMRON(self):
        print("***Doing OMRON***")

        #execfile("/Users/noebrito/OneDrive/Github_Pi/Omron/thermal-display.py")
        
    
    #**STUB METHOD**
    def toggleLED(self):
        print "Toggle LED"
    

    
        
