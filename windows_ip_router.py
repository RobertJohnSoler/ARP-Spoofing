import win32serviceutil
import time


# This class is responsible for enable ip routing in the attacker's computer

class IP_Router:

    def __init__(self):
        self.service = "RemoteAccess"
        
    def isRunning(self):
        return win32serviceutil.QueryServiceStatus(self.service)[1] == 4
    
    # Function to tell your machine to enable IP routing (if it's Windows)
    def start(self):
        if not self.isRunning():
            win32serviceutil.StartService(self.service)
            time.sleep(1)
            if self.isRunning:
                print("Remote access successfully started, IP routing now enabled.")
            else:
                print("Error starting remote access service.")
        elif self.isRunning():
            print(f"{self.service} is already running!")

    # Function to tell your machine to disable IP routing (if it's Windows)
    def stop(self):
        if self.isRunning():
            win32serviceutil.StopService(self.service)
            time.sleep(1)
            if not self.isRunning():
                print("Remote access service is now stopped. IP routing is disabled.")
            else:
                print("Error stopping remote access service.")
        elif not self.isRunning():
            print("Remote access is currently not running yet!")



