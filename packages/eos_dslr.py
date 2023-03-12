# MIT License

# Copyright (c) 2023 [Philippe Lopez]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import datetime
import logging
from ctypes import *
from packages.EDSDK_Class import *
from packages.toolkit import log_execution_time

edsdk = windll.edsdk

class EOS_DSLR:
    def __init__(self) -> None:
        logging.info("*** EOS_DSLR Initialization ***")
        self.cam = None
        self.list = c_void_p(None)
        self.count = c_int()
        self.cam = c_void_p()
        self.Edsdk_Status_Check('GetCameraList', edsdk.EdsGetCameraList(byref(self.list)))       
        self.Edsdk_Status_Check('GetChildCount', edsdk.EdsGetChildCount(self.list, byref(self.count)))        
        self.Edsdk_Status_Check('GetChildAtIndex', edsdk.EdsGetChildAtIndex(self.list, 0, byref(self.cam)))
        if self.count.value == 0:
            logging.critical("NO CAMERA FOUND. EXITING!")
            exit()
        elif self.count.value == 1:
            logging.info(f"Found {self.count.value} camera")
        else:
            logging.warning(f"Found {self.count.value} cameras")
            logging.warning("Will open a session with one of them...")

        if self.count.value != 0:
            logging.info(f"Opening a session with the camera...")
            self.Edsdk_Status_Check('OpenSession', edsdk.EdsOpenSession(self.cam))

            ObjectHandlerType = WINFUNCTYPE(c_int, c_int, c_void_p, c_void_p)
            def ObjectHandler_py(event, object, context):
                return event, object, context
            ObjectHandler = ObjectHandlerType(ObjectHandler_py)

            StateHandlerType = WINFUNCTYPE(c_int, c_int, c_int, c_void_p)
            def StateHandler_py(event, state, context):
                if event == StateEvent.Shutdown:
                    logging.critical("CAMERA IS DISCONNECTED")
                elif event == StateEvent.WillSoonShutDown:
                    logging.critical("CAMERA WILL SOON SHUTDOWN!!")
                return event, state, context
            StateHandler = StateHandlerType(StateHandler_py)

            PropertyHandlerType = WINFUNCTYPE(c_int, c_int, c_int, c_int, c_void_p)
            def PropertyHandler_py(event, property, param, context):
                print(event, property, param, context)
                return event, property, param, context
            PropertyHandler = PropertyHandlerType(PropertyHandler_py)        

            logging.info(f"Setting Object/Propert/State Events Handler with the camera...")
            self.Edsdk_Status_Check('SetObjectEventHandler', edsdk.EdsSetObjectEventHandler(self.cam, ObjectEvent.All, ObjectHandler, None))
            self.Edsdk_Status_Check('SetPropertyEventHandler', edsdk.EdsSetPropertyEventHandler(self.cam, PropertyEvent.All, PropertyHandler, None))
            self.Edsdk_Status_Check('SetCameraStateEventHandler', edsdk.EdsSetCameraStateEventHandler(self.cam, StateEvent.All, StateHandler, self.cam))

        logging.info("*** EOS_DSLR Initialization Completed ***")

    def __del__(self) -> None:
        if self.cam is not None:
            logging.info("Releasing the camera...")
            self.Edsdk_Status_Check('CloseSession', edsdk.EdsCloseSession(self.cam))
            self.Edsdk_Status_Check('Release', edsdk.EdsRelease(self.cam))
        edsdk.EdsRelease(self.list)

    def Edsdk_Status_Check(self, execution, err_code):
        if err_code in Error.Get:
            if Error.Get[err_code] != "OK":
                logging.critical(f"Error during {execution}: {Error.Get[err_code]}")
        else:
            logging.critical(f"Unknown Error Code during {execution}: {err_code}")

    # Dummy: Does not work!
    def GetProperty(self, property, property_name):
        c = c_void_p()
        err = edsdk.EdsGetPropertyData(self.cam, property, 0, byref(c))
        self.Edsdk_Status_Check(f"{property_name} Property Reading", err)
        return c.value

    def SetProperty(self, property, parameter, property_name='', start_time=None):
        c_int_parameter = c_int(parameter)
        err = edsdk.EdsSetPropertyData(self.cam, property, 0, 32, byref(c_int_parameter))
        while(Error.Get[err] == "DEVICE_BUSY"):
            err = edsdk.EdsSetPropertyData(self.cam,property, 0, 32, byref(c_int_parameter))
        self.Edsdk_Status_Check(f"{property_name} Property Setting", err)
        if start_time is not None:
            log_execution_time(execution=f"{property_name} Property Setting", start_time=start_time, end_time=time.time())

    def SingleShootAF(self, start_time=None):
        err = edsdk.EdsSendCommand(self.cam, Command.TakePicture, 0)
        while(Error.Get[err] == "DEVICE_BUSY"):
            err = edsdk.EdsSendCommand(self.cam, Command.TakePicture, 0)
        self.Edsdk_Status_Check("Single Shoot", err)
        if start_time is not None:
            log_execution_time(execution="Single Shoot AF", start_time=start_time, end_time=time.time())

    def BurstShootNonAF(self, duration=0, next_event_time=None, start_time=None):
        err = edsdk.EdsSendCommand(self.cam, Command.PressShutterButton, Command.ShutterButton_Completely_NonAF)
        while(Error.Get[err] == "DEVICE_BUSY"):
            err = edsdk.EdsSendCommand(self.cam, Command.PressShutterButton, Command.ShutterButton_Completely_NonAF)
        self.Edsdk_Status_Check("Burst Shoot", err)
        if next_event_time is not None:
            duration = max(0, min(duration, next_event_time - datetime.datetime.timestamp(datetime.datetime.utcnow())))
        time.sleep(duration)
        err = edsdk.EdsSendCommand(self.cam, Command.PressShutterButton, Command.ShutterButton_OFF)
        while(Error.Get[err] == "DEVICE_BUSY"):
            err = edsdk.EdsSendCommand(self.cam, Command.PressShutterButton, Command.ShutterButton_OFF)
        self.Edsdk_Status_Check("Burst Shoot", err)
        if start_time is not None:
            if duration == 0:
                log_execution_time(execution="Single Shoot NonAF", start_time=start_time, end_time=time.time())
            else:
                log_execution_time(execution="Burst Shoot", start_time=start_time, end_time=time.time())
