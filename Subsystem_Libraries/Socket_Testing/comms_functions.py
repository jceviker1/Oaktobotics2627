'''

TODO:
    - get_latency function
    - there has got to be a better way to organize the functions
    
'''
import time
import threading
import random
import socket


#-------------------CLASS DEFINITIONS------------------------------------------------------------------------------

class simplesocket:
    
    # HOST is what it's listening for. 0.0.0.0 is for all ip adresses (recomended)
    # Do not make listening and sending PORTs the same
    def __init__(self, HOST, PORT, begin=True, pause=0.1):
        self.HOST = HOST
        self.PORT = PORT

        self.start_time = 0.0
        self.lock = threading.Lock() # Idk why declare here vs outside the class, but I put it here bc claude did. Should work either way i think

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
        try:
            while True:
                try:
                    recv_data, addr = self.server.recvfrom(1024)
                except ConnectionResetError: # with windows, this bug shows up if it's sending and nobody is listening.
                    continue
                with self.lock:
                    self.new_data = recv_data.decode()
                    self.total_size += len(recv_data) * 8 / (1024 * 1024) # Size in Mb
                    self.peak_bandwidth = max(self.peak_bandwidth, self._get_bandwidth_nolock())
        except KeyboardInterrupt:
            self.close()
            print("Listener stopped.")
    
    def listen(self, pause=0.1):
        threading.Thread(target=self._listener, daemon=True).start()
        self.start_time = time.time()

        # this is to prevent peak bandwidth from spiking right at the start
        if pause > 0:
            time.sleep(pause)
        
        return self.start_time
    
    # always returns the newest data as a string, no matter how old it was
    def get_data(self):
        with self.lock:
            return self.new_data
    
    def clear_data(self):
        with self.lock:
            self.new_data = None

    # HOST and PORT are for the destination
    def send(self, data, HOST, PORT):
        send_data = str(data).encode()
        with self.lock:
            self.total_size += len(send_data) * 8 / (1024 * 1024) # Size in Mb
            self.peak_bandwidth = max(self.peak_bandwidth, self._get_bandwidth_nolock())
        self.server.sendto(send_data, (HOST, PORT))
    
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
        self.server.close()
