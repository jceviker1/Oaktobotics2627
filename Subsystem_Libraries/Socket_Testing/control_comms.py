# Old file. Not very useful anymore
import time
import threading
import random
import socket

new_data = None
data = None
lock = threading.Lock()
start_time = 0.0
total_size = 0.0
peak_latency = 0.0
peak_bandwidth = 0.0

# Define IP adresses and ports for communication
CONTROL_HOST = '0.0.0.0'  # listen on all interfaces
CONTROL_PORT = 56666
PIT_HOST = '127.0.0.1'  # IP address of the pit computer (local host for now)
PIT_PORT = 55555

# Create and bind socket to listen for incoming data from pit computer
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((CONTROL_HOST, CONTROL_PORT))
print(f"Now listening on port {CONTROL_PORT}")

def listener():
    global new_data
    try:
        while True:
            recv_data, addr = s.recvfrom(1024)
            with lock:
                new_data = recv_data.decode()
    except KeyboardInterrupt:
        print("Listener stopped.")

# Begin listening thread
t1 = threading.Thread(target=listener, daemon=True)
t1.start()
start_time = time.time()

try:
    while True:
        # Recieve data
        with lock:
            if new_data is not None:
                data = new_data
                new_data = None
            else:
                data = None
        
        # Process data
        if data is not None:
            timestamp = time.time() - start_time
            data_size = len(data.encode()) * 8  # Size in bits
            total_size += (data_size / (1024 * 1024))  # Convert to Mb
            latency = 0.0  # TODO: Implement actual latency measurement
            bandwidth = total_size / timestamp if timestamp > 0 else 0  # Mbps
            #peak_latency = max(peak_latency, latency)
            peak_bandwidth = max(peak_bandwidth, bandwidth)
            print(f"R: {data_size:.2f} b    T: {timestamp:.2f} s    L: {latency:.2f} s    PL: {peak_latency:.2f} s    B: {bandwidth:.2f} Mbps    PB: {peak_bandwidth:.2f} Mbps")
        
        time.sleep(0.1)  # Sleep briefly to reduce CPU usage
except KeyboardInterrupt:
    print("Main thread stopped.")
finally:
    s.close()

    # Print final diagnostics
    print(f"Total data received: {total_size:.2f} Mb")
    print(f"Peak latency: {peak_latency:.2f} seconds")
    print(f"Peak bandwidth: {peak_bandwidth:.2f} Mbps")
