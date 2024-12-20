# ARP Spoofing

This repo contains Python code for carrying out an Man-In-The-Middle (MITM) attack called "ARP Spoofing". Though MITM attacks are usually used for nasty purposes, this repo should be used for educational purposes only. <strong> MAKE SURE THAT YOU TEST THIS IN A CONTROLLED ENVIRONMENT WITH PROPER PERMISSIONS!</strong> 
<br>

To execute this attack, both your attacker machine (the computer that runs the code in this repo) and your test victim machine should be in the same network. 

The attack in this repo is supported on Windows and Linux.

To carry out the attack using a Windows machine, run this command:<br>
`python3 Arp_Spoofer.py --target <target ipv4> --gateway <router's gateway ipv4> -c eth`