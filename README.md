# ARP Spoofing
## Overview
This repo contains Python code for carrying out an Man-In-The-Middle (MITM) attack called "ARP Spoofing". Though MITM attacks are usually used for nasty purposes, this repo should be used for educational purposes only. Using this code for illegal actions is punishable by law. <strong> MAKE SURE THAT YOU TEST THIS IN A CONTROLLED ENVIRONMENT WITH PROPER PERMISSIONS!</strong> 
<br>

To execute this attack, both your attacker machine (the computer that runs the code in this repo) and your test victim machine should be in the same network. 

The attack in this repo is supported on Windows and Linux.

## Requirements and Prerequisites
1. Make sure Python 3.11 (or later) and pip are installed in your computer.
2. Run these commands to install the required dependencies:
```
    pip install scapy
    pip install pywin32
```
3. Enable routing on your computer (for Windows machines only). 
    - On the Windows search bar, search for and open services.msc.
    - Locate "Routing and Remote Access", right-click it, select Properties.
    - Change the startup type to either manual or automatic. Make sure it isn't disabled.
    - Click Apply and then Ok, then close the window.

## Options
Below are the different options you can use when running this script:
```
options:
  -h, --help                            show this help message and exit
  -t TARGET_IP, --target TARGET_IP      Target IP address
  -g GATEWAY_IP, --gateway GATEWAY_IP   Gateway IP address
  -c CON_MODE, --connection CON_MODE    Connection mode [wifi or eth]
  -o OP_MODE, --op_mode OP_MODE         What you want to accomplish with ARP spoofing [wifi_cut or MITM]
```
* `con_mode` refers to how your attacker's machine is connected to the network. 
    * If your attacker's machine is connected via ethernet cable, use `-c eth`. 
    * If your attacker's machine is connected via wifi, use `-c wifi`. When using this, make sure that you have a wifi adapter capable of monitor mode.
* `op_mode` refers to the kind of MITM attack you want to execute. As of now, this repo supports two attacks:
     * `wifi_cut` cuts your victim's internet connection. Their machine will think that it's still connected to the WIFI network, but they are actually no longer connected to the internet. This is the default attack.
     * `MITM` does a classic MITM attack on your victim. All the internet traffic that the victim is generating and receiving will pass through your computer first.

### Examples
To carry out a wifi_cut attack using a machine that's connected via ethernet, run this command:
```
python3 Arp_Spoofer.py --target <target ipv4> --gateway <router's gateway ipv4> -c eth -o wifi_cut
```

To carry out an MITM attack using a machine that's connected via WIFI, run this command:
```
python3 Arp_Spoofer.py --target <target ipv4> --gateway <router's gateway ipv4> -c wifi -o MITM
```

## Limitations
1. Unfortunately, this attack fully works against computers that use IPv4 only. If your victim machine is also using IPv6, then it will still be able to visit sites that support IPv6. However, not all sites support IPv6 yet. Some support IPv4 only, so the victim machine won't be able to connect to them. Good examples are Steam, Github, and Twitch.
2. To be able to use the `-c wifi` and `-o MITM` args, your attacker machine will need to have a WIFI adapter capable of monitor mode. Unfortunately, the WIFI adapter I had only supported Linux, so I wasn't able to test if `-c wifi` worked when using Windows. You could try it out for yourself, though.
3. Sometimes, your victim laptop will have an ARP cache that stores the last working MAC addresses in case it's given one that doesn't work. This could cause your wifi_cut to fail. If that happens, clear the ARP cache on your victim computer using the command `arp -d *`.