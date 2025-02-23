import os
import sys
import time
from bluetooth import *
#import logging
#import threading

server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
advertise_service(server_sock, "RaspberryPiService",
                  service_classes=[SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE])

print(f"Waiting for connection on RFCOMM channel {port}...")
os.system("bluetoothctl discoverable on")

client_sock, client_info = server_sock.accept()
print(f"Connected to {client_info}")
os.system("bluetoothctl discoverable off")

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print(f"Received: {data.decode('utf-8')}")
        client_sock.send("Message received!".encode('utf-8'))
except OSError:
    pass

print("Disconnected")
client_sock.close()
server_sock.close()
os.system("bluetoothctl discoverable on")  # Make discoverable again after disconnection
