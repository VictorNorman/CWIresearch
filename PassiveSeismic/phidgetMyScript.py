# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 16:13:01 2020

@author: Jim Clark
"""

import sys
import time
import traceback

from Phidget22.Devices.Accelerometer import *
from Phidget22.PhidgetException import *
from Phidget22.ErrorCode import *
from Phidget22.Phidget import *
from Phidget22.Net import *
import pandas as pd
import matplotlib.pyplot as plt

xAccel=[]
yAccel=[]
zAccel=[]
sensorTime=[]

totalTime_minutes=input('EnterInput the total recording time in minutes  ')
dataInterval_ms=input('Enter the data interval in milliseconds e.g. 4  ')


class EndProgramSignal(Exception):
    def __init__(self, value):
        self.value = str(value )  
        
def PrintOpenErrorMessage(e, ph):
    sys.stderr.write("Runtime Error -> Opening Phidget Channel: \n\t")
    DisplayError(e)
    if(e.code == ErrorCode.EPHIDGET_TIMEOUT):
        sys.stderr.write("\nThis error commonly occurs if your device is not connected as specified, "
                         "or if another program is using the device, such as the Phidget Control Panel.\n")
        sys.stderr.write("\nIf your Phidget has a plug or terminal block for external power, ensure it is plugged in and powered.\n")
        if(     ph.getChannelClass() != ChannelClass.PHIDCHCLASS_VOLTAGEINPUT
            and ph.getChannelClass() != ChannelClass.PHIDCHCLASS_VOLTAGERATIOINPUT
            and ph.getChannelClass() != ChannelClass.PHIDCHCLASS_DIGITALINPUT
            and ph.getChannelClass() != ChannelClass.PHIDCHCLASS_DIGITALOUTPUT
        ):
            sys.stderr.write("\nIf you are trying to connect to an analog sensor, you will need to use the "
                              "corresponding VoltageInput or VoltageRatioInput API with the appropriate SensorType.\n")
                              
        if(ph.getIsRemote()):
            sys.stderr.write("\nEnsure the Phidget Network Server is enabled on the machine the Phidget is plugged into.")

def DisplayError(e):
    print("Desc: " + e.details + "\n")
    
    if (e.code == ErrorCode.EPHIDGET_WRONGDEVICE):
        sys.stderr.write("\tThis error commonly occurs when the Phidget function you are calling does not match the class of the channel that called it.\n"
                        "\tFor example, you would get this error if you called a PhidgetVoltageInput_* function with a PhidgetDigitalOutput channel.")
    elif (e.code == ErrorCode.EPHIDGET_NOTATTACHED):
        sys.stderr.write("\tThis error occurs when you call Phidget functions before a Phidget channel has been opened and attached.\n"
                        "\tTo prevent this error, ensure you are calling the function after the Phidget has been opened and the program has verified it is attached.")
    elif (e.code == ErrorCode.EPHIDGET_NOTCONFIGURED):
        sys.stderr.write("\tThis error code commonly occurs when you call an Enable-type function before all Must-Set Parameters have been set for the channel.\n"
                        "\tCheck the API page for your device to see which parameters are labled \"Must be Set\" on the right-hand side of the list.")
"""
* Configures the device's DataInterval and ChangeTrigger.
* Displays info about the attached Phidget channel.
* Fired when a Phidget channel with onAttachHandler registered attaches
*
* @param self The Phidget channel that fired the attach event
"""
def onAttachHandler(self):
    
    ph = self
    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information
        
        print("\nAttach Event:")
 
        ph.setDeviceSerialNumber(419779)
        ph.setChannel(0)
        #ph.setChannelClassName('Accelerometer')
#        
        """
        * Set the DataInterval inside of the attach handler to initialize the device with this value.
        * DataInterval defines the minimum time between AccelerationChange events.
        * DataInterval can be set to any value from MinDataInterval to MaxDataInterval.
        """
        print("\n\tSetting DataInterval to 5ms")
        ph.setDataInterval(int(dataInterval_ms))

        """
        * Set the AccelerationChangeTrigger inside of the attach handler to initialize the device with this value.
        * AccelerationChangeTrigger will affect the frequency of AccelerationChange events, by limiting them to only occur when
        * the acceleration changes by at least the value set.
        """
        #print("\tSetting Acceleration ChangeTrigger to 0.05")
        ph.setAccelerationChangeTrigger(0.0)

    except PhidgetException as e:
        print("\nError in Attach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

"""
* Displays info about the detached Phidget channel.
* Fired when a Phidget channel with onDetachHandler registered detaches
*
* @param self The Phidget channel that fired the attach event
"""
def onDetachHandler(self):

    ph = self
    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information
    
        print("\nDetach Event:")
        
        """
        * Get device information and display it.
        """
#        serialNumber = ph.getDeviceSerialNumber()
#        channelClass = ph.getChannelClassName()
#        channel = ph.getChannel()
        ph.setDeviceSerialNumber(419779)
        ph.setChannelClassName('Accelerometer')
        ph.setChannel(0)
        
        
    except PhidgetException as e:
        print("\nError in Detach Event:")
        DisplayError(e)
        traceback.print_exc()
        return


"""
* Writes Phidget error info to stderr.
* Fired when a Phidget channel with onErrorHandler registered encounters an error in the library
*
* @param self The Phidget channel that fired the attach event
* @param errorCode the code associated with the error of enum type ph.ErrorEventCode
* @param errorString string containing the description of the error fired
"""
def onErrorHandler(self, errorCode, errorString):

    print("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

"""
* Outputs the Accelerometer's most recently reported acceleration.
* Fired when a Accelerometer channel with onAccelerationChangeHandler registered meets DataInterval and ChangeTrigger criteria
*
* @param self The Accelerometer channel that fired the AccelerationChange event
* @param acceleration The reported acceleration from the Accelerometer channel
"""
def onAccelerationChangeHandler(self, acceleration, timestamp):
    global xAccel, yAccel, zAccel, countit
#    countit=countit+1
#    if countit<150:
#        print("[Acceleration Event] -> Acceleration: %f %f %f" % (acceleration[0], acceleration[1], acceleration[2]))
#        print("                      -> Timestamp   : %f\n" % timestamp)
#    else:
#        strvar=input('this stops it for a bit')
    #print("[Acceleration Event] -> Acceleration: %f %f %f" % (acceleration[0], acceleration[1], acceleration[2]))
    #print("                      -> Timestamp   : %f\n" % timestamp)
    xAccel.append(acceleration[0])
    yAccel.append(acceleration[1])
    zAccel.append(acceleration[2])
    sensorTime.append(timestamp)
    
def WriteFile():
    global xAccel, yAccel, zAccel, countit
    print("i am writing a file now")
    
#    textvar=plt.figtext(0.2,0.13,'Writing File')        
#    textvar.set_visible(True)
#    plt.pause(0.1)
    
    csvFile = open("phidgetFile1.csv", "w") 
    
    df = pd.DataFrame({"aTime" : sensorTime, "bx-Axis" : xAccel,\
            "cy-Axis" : yAccel,"dz-Axis" :zAccel})
    df.to_csv(csvFile, index=False)
    
    csvFile.close()
    print("I finished writing the file")
#    textvar.set_visible(False)
#    plt.pause(0.1)
def plotFile():
    global xAccel, yAccel, zAccel, countit
    print("i am plotting now")
    plt.figure(1)
    plt.plot(sensorTime,zAccel)
    plt.show()

"""
* Creates, configures, and opens a Accelerometer channel.
* Displays Acceleration events for 10 seconds
* Closes out Accelerometer channel
*
* @return 0 if the program exits successfully, 1 if it exits with errors.
"""
def main():
    try:
        """
        * Allocate a new Phidget Channel object
        """
        try:
            ch = Accelerometer()
        except PhidgetException as e:
            print("Runtime Error -> Creating Accelerometer: \n\t")
            DisplayError(e)
            raise
        except RuntimeError as e:
            print("Runtime Error -> Creating Accelerometer: \n\t" + e)
            raise

        """
        * Set matching parameters to specify which channel to open
        """
    
        ch.setDeviceSerialNumber(419779)
        ch.setHubPort(-1)
        ch.setChannel(0)   
        
        """
        * Add event handlers before calling open so that no events are missed.
        """
        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch.setOnAttachHandler(onAttachHandler)
        
        print("Setting OnDetachHandler...")
        ch.setOnDetachHandler(onDetachHandler)
        
        print("Setting OnErrorHandler...")
        ch.setOnErrorHandler(onErrorHandler)
        
        print("\nSetting OnAccelerationChangeHandler...")
        ch.setOnAccelerationChangeHandler(onAccelerationChangeHandler)
        
        """
        * Open the channel with a timeout
        """
        
        print("\nOpening and Waiting for Attachment...")
        
        try:
            ch.openWaitForAttachment(5000)
        except PhidgetException as e:
            PrintOpenErrorMessage(e, ch)
            raise EndProgramSignal("Program Terminated: Open Failed")
        
        #print("Sampling data for 10 seconds...")
        
        print("You can do stuff with your Phidgets here and/or in the event handlers.")
        
        
        time.sleep(float(totalTime_minutes)*60)
        
        """
        * Perform clean up and exit
        """

        #clear the AccelerationChange event handler 
        ch.setOnAccelerationChangeHandler(None)
        
        WriteFile()
        plotFile()
        print("\nDone Sampling...")

        print("Cleaning up...")
        ch.close()
        print("\nExiting...")
        return 0

    except PhidgetException as e:
        sys.stderr.write("\nExiting with error(s)...")
        DisplayError(e)
        traceback.print_exc()
        print("Cleaning up...")
        ch.setOnAccelerationChangeHandler(None)
        ch.close()
        return 1
    except EndProgramSignal as e:
        print(e)
        print("Cleaning up...")
        ch.setOnAccelerationChangeHandler(None)
        ch.close()
        return 1
    finally:
        #print("Press ENTER to end program.")
        readin = input('press enter to end program')

main()

