# This class is responsible for enable ip routing in the attacker's computer (if it's running on Linux)

class Linux_IP_Router():

    def __init__(self):
        self.file_path = "/proc/sys/net/ipv4/ip_forward"

    # Function to tell your machine to enable IP routing
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

    # Function to tell your machine to stop IP routing
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