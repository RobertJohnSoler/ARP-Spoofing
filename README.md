# ARP Spoofing
## Overview
This repo contains Python code for carrying out an Man-In-The-Middle (MITM) attack called "ARP Spoofing". Though MITM attacks are usually used for nasty purposes, this repo should be used for educational purposes only. Using this code for illegal actions is punishable by law. <strong> MAKE SURE THAT YOU TEST THIS IN A CONTROLLED ENVIRONMENT WITH PROPER PERMISSIONS!</strong> 
<br>

To execute this attack, both your attacker machine (the computer that runs the code in this repo) and your test victim machine should be in the same network. 

The attack in this repo is supported on Windows and Linux.

To carry out the attack using a Windows machine, run this command:<br>
`python3 Arp_Spoofer.py --target <target ipv4> --gateway <router's gateway ipv4> -c eth`

## Requirements and Prerequisites
1. Make sure Python 3.11 (or later) and pip are installed in your computer.
2. Run these commands to install the required dependencies:
```
    pip install scapy
    pip install pywin32
```
3. Enable routing on your computer. 
    - On the Windows search bar, search for and open services.msc.
    - Locate "Routing and Remote Access", right-click it, select Properties.
    - Change the startup type to either manual or automatic. Make sure it isn't disabled.
    - Click Apply and then Ok, then close the window.