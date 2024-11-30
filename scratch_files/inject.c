#include <stdio.h>
#include <pcap.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#define TIMEOUT 5 

void packet_handler(unsigned char *user_data, const struct pcap_pkthdr *pkthdr, const unsigned char *packet) {
    // The MAC address we expect the ACK to be from (the sender of the "Hello!" message)
    const unsigned char *dest_mac = (const unsigned char *)user_data;

    // Check if the packet is an ACK frame (Frame Control: 0xD4 - 11010000)
    // ACK frame has Frame Control = 0xD4 and Type = 0x1D (ACK)
    if (packet[0] == 0xD4) {
        // Check if the destination MAC in the packet is the source MAC of our sent message
        if (memcmp(&packet[4], dest_mac, 6) == 0) {
            printf("Received ACK for the 'Hello!' message.\n");
        }
    }
}

int main(){
    char *interface = "wlan0mon";       // the interface you want to use to inject packets
    char errbuf[PCAP_ERRBUF_SIZE];      // just a buffer to hold the error message, if any
    pcap_t *handler = pcap_open_live(interface, BUFSIZ, 1, 1000, errbuf); // enable the chosen interface to handle the capturing and sending of packets
    const char* dest_MAC = "\xf6\xc1\x14\xf9\xec\xb6";
    const char* source_MAC = "\xc0\x1c\x30\x2f\xf9\x17";
    const char* BSSID = "\xec\x5c\x68\x4a\xdb\x33";
    const char* msg = "Hello!";

    if (handler == NULL){               // check if the device was enabled successfully
        printf("Error opening device!");
    } else {
        printf("%s ready for packet injection.", interface);
    }

    // create the packet that will be injected
    unsigned char packet[128];

    // frame control
    packet[0] = 0x08;        // 0x08 is the field that specifies that this is a data frame, since we are sending a simple "hello" message
    packet[1] = 0x02;        // flags telling signifiying that this packet came from a distributor, such as a router or an access point

    // duration/id
    packet[2] = 0x00;
    packet[3] = 0x00;

    // addresses involved
    memcpy(&packet[4], "\xec\x5c\x68\x4a\xdb\x33", 6);
    memcpy(&packet[10], "\xf6\xc1\x14\xf9\xec\xb6", 6);
    memcpy(&packet[16], "\xf6\xc1\x14\xf9\xec\xb6", 6);

    // sequence control
    packet[22] = 0x00;
    packet[23] = 0x00;

    // payload, or the message we are trying to send
    memcpy(&packet[24], msg, strlen(msg));

    // sending the packet
    int send_status = pcap_sendpacket(handler, packet, 24+strlen(msg));
    if (send_status != 0 ){
        printf("Error sending packet!");
        return 1;
    } else {
        printf("Message %s sent!", msg);
    }

    printf("Waiting for ACK...\n");

    // Set up the capture to check for ACK
    pcap_loop(handler, 0, packet_handler, (unsigned char *)dest_MAC);

    pcap_close(handler);
    return 0;
}