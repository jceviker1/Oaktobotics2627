import time
import threading
import random
import socket

new_data = None
data = None
lock = threading.Lock()

# Define IP addresses and ports for communication
PIT_HOST = '0.0.0.0'  # listen on all interfaces
PIT_PORT = 55555
CONTROL_HOST = '127.0.0.1'  # IP address of the control computer (local host for now)
CONTROL_PORT = 56666

# Create and bind socket to listen for incoming data from control computer
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((PIT_HOST, PIT_PORT))
print(f"Now listening on port {PIT_PORT}")


def listener():
    global new_data
    try:
        while True:
            recv_data, addr = s.recvfrom(1024)
            with lock: # use lock to prevent data corruption when accessing new_data
                new_data = recv_data.decode()
    except KeyboardInterrupt:
        print("Listener thread stopped.")

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
            print(f"Main thread received: {data}    Time Elapsed: {timestamp:.2f} seconds")
            data = None
        
        # send random data back to the sender for testing
        s.sendto(f"{random.randint(10, 99)}".encode(), (CONTROL_HOST, CONTROL_PORT))

        time.sleep(0.1)  # Sleep briefly to reduce CPU usage
except KeyboardInterrupt:
    print("Main thread stopped.")
finally:
    s.close()
