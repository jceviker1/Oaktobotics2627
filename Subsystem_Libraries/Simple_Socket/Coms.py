'''
To use:
    1. Initiate a socket server with a command such as:
       server = SocketServer("0.0.0.0", 12345)
    2. Send data to the server using the send_data function:
       send_data("Hello, server!", ("Destination IP as a String", 12345))
    3. Retrieve data (as a String) from the server using the get_data function:
       some_awesome_new_data = server.get_data()
    4. Clear any old data from the server using the clear_data function:
       server.clear_data()
    5. Get statistics like Bandwidth, Peak Bandwidth, and Latency (TODO) with the appropriate functions
            (Bandwidth (Mbps) is counted when it is recieved by a socket. Send bandwidth is not counted.)
    6. Close the server using the close function:
       server.close()

TODO:
    - get_latency function
    - the code can work for video, but doing so will use a lot more bandwidth. Use something like H.264 or H.265 for efficient video transmission.
    - _listener does not properly stop and close the server because ctrl+c is not caught by threads
    
'''
import time
import threading
import random
import socket


#-------------------CLASS DEFINITIONS------------------------------------------------------------------------------

class SocketServer:
    
    # HOST is what it's listening for. 0.0.0.0 is for all ip adresses (recomended)
    # Do not make listening and sending PORTs the same
    # bytes is how many bytes the socket will be recieving at once. If a message is longer, it gets truncated. Max bytes is 65535
    def __init__(self, HOST, PORT, bytes=1024, begin=True, pause=0.1):
        self.HOST = HOST
        self.PORT = PORT

        self.start_time = 0.0
        self.bytes = bytes
        self.lock = threading.Lock()

        self._running = threading.Event()
        self._running.set()

        # always use lock for these variables
        self.new_data = None
        self.total_size = 0.0
        self.peak_bandwidth = 0.0 # Mbps

        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.HOST, self.PORT))

        if begin:
            self.listen(pause)

    # Only use this when already in a lock
    def _get_bandwidth_nolock(self):
        timestamp = time.time() - self.start_time
        return self.total_size / timestamp if timestamp > 0 else 0

    def _listener(self):
        while self._running.is_set():
            try:
                recv_data, addr = self.server.recvfrom(self.bytes)
            except ConnectionResetError: # with windows, this bug shows up if it's sending and nobody is listening.
                continue
            except OSError:
                print("Server does not exist, ", end="")
                break
            with self.lock:
                self.new_data = recv_data.decode()
                self.total_size += len(recv_data) * 8 / (1024 * 1024) # Size in Mb
                self.peak_bandwidth = max(self.peak_bandwidth, self._get_bandwidth_nolock())
        print("Listener stopped.")
    
    def listen(self, pause=0.1):
        threading.Thread(target=self._listener, daemon=True).start()
        self.start_time = time.time()

        # this is to prevent peak bandwidth from spiking right at the start
        # technically bandwidth is still spiking, but nasa only meassures average, so this does actually work
        if pause > 0:
            time.sleep(pause)

        print("Listener started.")
        
        return self.start_time
    
    # always returns the newest data as a string, no matter how old it was
    def get_data(self):
        with self.lock:
            return self.new_data
    
    def clear_data(self):
        with self.lock:
            self.new_data = None
    
    def get_bandwidth(self):
        with self.lock:
            timestamp = time.time() - self.start_time
            return self.total_size / timestamp if timestamp > 0 else 0  # Mbps
    
    def get_peak_bandwidth(self):
        with self.lock:
            return self.peak_bandwidth
    
    def get_total_size(self):
        with self.lock:
            return self.total_size
    
    def close(self):
        self._running.clear()
        self.server.close()

# ------------------Functions--------------------------------------------------------------------------------------

# addr is a tuple containing the host and port. Use the IP address of the destination.
# if data is too large, it will be cut off
# data is a string
def send_data(data, addr):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(data.encode(), addr)