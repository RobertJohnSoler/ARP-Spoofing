/* Compile with: gcc find_device.c -lpcap */
#include <stdio.h>
#include <pcap.h>

int main() {
    
    char error_buffer[PCAP_ERRBUF_SIZE]; /* Size defined in pcap.h */
    pcap_if_t *interface_list;

    /* Find a device */
    int devices = pcap_findalldevs(&interface_list, error_buffer);
    if (devices != 0) {
        printf("Error finding device: %s\n", error_buffer);
        return 1;
    }

    for(pcap_if_t *i = interface_list; i!= NULL; i=i->next)
    {
        printf("Name: %s (%s)\n", i->name, i->description);
    }
     pcap_freealldevs(interface_list);
     return 1;
}