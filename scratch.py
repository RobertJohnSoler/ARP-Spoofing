from spoofing_services import *

enableIPRoute("Linux")
print(getMac("", "wlan0"))
disableIPRoute("Linux")