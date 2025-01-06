# This file 

class Linux_IP_Router():

    def __init__(self):
        self.file_path = "/proc/sys/net/ipv4/ip_forward"

    def start(self):
        """
        Enables IP route ( IP Forward ) in linux-based distro
        """
        self.file_path = "/proc/sys/net/ipv4/ip_forward"
        with open(self.file_path) as f:
            if f.read() == 1:
                # already enabled
                return
        with open(self.file_path, "w") as f:
            print(1, file=f)


    def stop(self):
        """
        Enables IP route ( IP Forward ) in linux-based distro
        """
        self.file_path = "/proc/sys/net/ipv4/ip_forward"
        with open(self.file_path) as f:
            if f.read() == 0:
                # already disabled
                return
        with open(self.file_path, "w") as f:
            print(0, file=f)