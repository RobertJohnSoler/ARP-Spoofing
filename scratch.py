from spoofing_services import *

enableIPRoute("Linux")
print(getMac("10.0.0.184", "wlan0"))
disableIPRoute("Linux")