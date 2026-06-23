'''

TODO:
    - get_latency function
    - actually test the code
    - there has got to be a better way to organize the functions
    
'''
import time
import threading
import random
import socket


#-------------------CLASS DEFINITIONS------------------------------------------------------------------------------

class simple_socket:
    
    # HOST is what it's listening for. 0.0.0.0 is for all ip adresses (recomended)
    # Do not make listening and sending PORTs the same
    def __init__(self, HOST, PORT, begin=True):
        self.HOST = HOST
        self.PORT = PORT

        self.start_time = 0.0
        self.lock = threading.Lock() # Idk why declare here vs outside the class, but I put it here bc claude did. Should work either way i think

        # always use lock for these variables
        self.new_data = None
        self.total_size = 0.0
        self.peak_bandwidth = 0.0 # Mbps

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.HOST, self.PORT))

        if begin:
            self.listen()

    # Only use this when already in a lock
    def _get_avg_bandwidth_nolock(self):
        timestamp = time.time() - self.start_time
        return self.total_size / timestamp if timestamp > 0 else 0

    def _listener(self):
        try:
            while True:
                recv_data, addr = self.s.recvfrom(1024)
                with self.lock:
                    self.new_data = recv_data.decode()
                    self.total_size += len(recv_data) * 8 / (1024 * 1024) # Size in Mb
                    self.peak_bandwidth = max(self.peak_bandwidth, self._get_avg_bandwidth_nolock())
        except KeyboardInterrupt:
            self.close()
            print("Listener stopped.")
    
    def listen(self):
        threading.Thread(target=self._listener, daemon=True).start()
        self.start_time = time.time()
        return self.start_time
    
    def get_data(self):
        with self.lock:
            return self.new_data

    # HOST and PORT are for the destination
    def send_data(self, data, HOST, PORT):
        send_data = data.encode()
        with self.lock:
            self.total_size += len(send_data) * 8 / (1024 * 1024) # Size in Mb
            self.peak_bandwidth = max(self.peak_bandwidth, self._get_avg_bandwidth_nolock())
        self.s.sendto(send_data, (HOST, PORT))
    
    def get_avg_bandwidth(self):
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
        self.s.close()