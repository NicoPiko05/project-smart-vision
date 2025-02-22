import os
import sys
import time
#import logging
#import threading

sys.path.append(os.path.expanduser("~/Documents/bluepy"))
from bluepy import btle

class BluetoothService:
    def __init__(self, name="SmartGlasses"):
        self.name = name
        self.advertise_service()

    def advertise_service(self):
        os.system("sudo hciconfig hci0 up")
        os.system("sudo hciconfig hci0 piscan")
        os.system(f"sudo hciconfig hci0 name {self.name}")
        os.system("sudo sdptool add SP")
        os.system("sudo rfcomm watch hci0")

    def start(self):
        print(f"{self.name} is now discoverable and connectable.")

if __name__ == "__main__":
    bt_service = BluetoothService()
    bt_service.start()
    while True:
        time.sleep(60)
