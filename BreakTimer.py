import datetime as dt
from math import ceil

class BreakTimer():

    def __init__(self):
        self.displayString = "0"
        self.manualOverrideFlag = False
        self.manualPresenceIndicator = False
        self.isTimeExpired = False
        self.textLengthErrorFlag = False
        self.returnTime = 0 #mins
        
    def clearDisplay(self):
        self.textLengthErrorFlag = False
        self.displayString = "0"
        self.inputDisplayString = "0"
        
        
        
    def updateDisplayString(self,anInt):
        if self.displayString == "0":
            self.displayString = str(anInt)
        else:
            if len(self.displayString) < 2:
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
    
    
#     def startBreak(self,breakLength,lock,isTimerDone,mainScreen,breakScreen):
#         mainScreen.grid_forget()
#         breakScreen.grid()
#         clockStart = dt.datetime.now()
#         clockExp = clockStart + dt.timedelta(minutes=int(breakLength))
#         
#         if breakLength == 0:
#             isTimerDone = 1
#         else:
#             isTimerDone = 0
#             
#         #Check to see if time expired. If so, set flag.
#         while isTimerDone == 0:
#             clockCur = dt.datetime.now()
#             clockRem = (clockExp - clockCur).total_seconds()
#             breakLength = ceil(clockRem/60)
#             print("clockRem: {0}".format(str(clockRem)))
#             lock.acquire()
#             print("ReturnTime: {0}".format(breakLength))
#             lock.release()
#             if clockRem <= 0:
#                 isTimerDone = 1
    
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
    
    
        #**STUB METHOD**
    def omronInput(self):
        print "process omron data or read in omron data determination"
        #logic, then call toggleLED
    
    #**STUB METHOD**
    def toggleLED(self):
        print "Toggle LED"
    
    #**UTILITY METHODS**
    
    #remove unnecessary data
    #input: 15:34:58.856000
    #output: 15:34:58
    
    
    
#     def formatTime(self,time):
#         aFlag = True #flag used to exit while loop
#         ii = 0 #counter used to iterate through string
#         formattedTime = "" #output of this utility function
#         
#         while(aFlag):
#             if (str(time)[ii] != "."):
#                 formattedTime+=str(time)[ii]
#                 ii+=1
#             else:
#                 aFlag = False #exit while loop
#         
#         return formattedTime
                
    
        
