#include <stdio.h>
#include <pcap.h>
#include <stdlib.h>
#include <string.h>


int main(){
    char* interface = "wlan0mon";       // the interface you want to use to inject packets
    char errbuf[PCAP_ERRBUF_SIZE];      // just a buffer to hold the error message, if any
    pcap_t *handler = pcap_open_live(interface, BUFSIZ, 1, 1000, errbuf); // enable the chosen interface to handle the capturing and sending of packets

    if (handler == NULL){               // check if the device was enabled successfully
        printf("Error opening device!");
        return 1;
    } else {
        printf("%s ready for packet injection.", interface);
        return 1;
    }

}