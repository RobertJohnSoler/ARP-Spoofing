#include <stdio.h>
#include <pcap.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define TIMEOUT 5 // Timeout in seconds to wait for ACK

// Function to handle the captured packet and check if it's an ACK
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

int main() {
    const char *interface = "wlan0mon";       // the interface you want to use to inject packets
    char errbuf[PCAP_ERRBUF_SIZE];      // just a buffer to hold the error message, if any
    pcap_t *handler = pcap_open_live(interface, BUFSIZ, 1, 1000, errbuf); // open device for capturing and injecting

    const char *dest_MAC = "\xec\x5c\x68\x4a\xdb\x33"; // receiver's MAC address
    const char *source_MAC = "\xc0\x1c\x30\x2f\xf9\x17"; // source MAC (Kali Linux VM's MAC)
    const char *BSSID = "\xf6\xc1\x14\xf9\xec\xb5"; // router's MAC (usually the BSSID)
    const char *msg = "Hello!";  // message payload

    if (handler == NULL) { // check if the device was enabled successfully
        printf("Error opening device!\n");
        return 1;
    } else {
        printf("%s ready for packet injection.\n", interface);
    }

    // Create the Radiotap header
    unsigned char radiotap_header[] = {
        0x00, 0x00,    // Radiotap version and padding
        0x08, 0x00,    // Radiotap header length (8 bytes)
        0x00, 0x00, 0x00, 0x00, // Flags (no specific flags set)
    };

    // Create the packet that will be injected
    unsigned char packet[128];

    // Add Radiotap header to the packet
    memcpy(packet, radiotap_header, sizeof(radiotap_header));

    // Frame control
    packet[sizeof(radiotap_header)] = 0x08; // 0x08 for data frame
    packet[sizeof(radiotap_header) + 1] = 0x02; // flags for the frame (data from AP)
    
    // Duration/ID
    packet[sizeof(radiotap_header) + 2] = 0x00;
    packet[sizeof(radiotap_header) + 3] = 0x00;

    // Addresses involved
    memcpy(&packet[sizeof(radiotap_header) + 4], dest_MAC, 6);   // Destination MAC
    memcpy(&packet[sizeof(radiotap_header) + 10], source_MAC, 6); // Source MAC
    memcpy(&packet[sizeof(radiotap_header) + 16], BSSID, 6);     // BSSID (router MAC)

    // Sequence control
    packet[sizeof(radiotap_header) + 22] = 0x00;
    packet[sizeof(radiotap_header) + 23] = 0x00;

    // Payload (message to send)
    memcpy(&packet[sizeof(radiotap_header) + 24], msg, strlen(msg));

    // Sending the packet
    int send_status = pcap_sendpacket(handler, packet, sizeof(radiotap_header) + 24 + strlen(msg));
    if (send_status != 0) {
        printf("Error sending packet!\n");
        return 1;
    } else {
        printf("Message '%s' sent!\n", msg);
    }

    // Now, we wait for an ACK frame
    printf("Waiting for ACK...\n");

    // Set up the capture to check for ACK
    pcap_loop(handler, 0, packet_handler, (unsigned char *)dest_MAC);

    // Close the handler when done
    pcap_close(handler);
    return 0;
}
