#!/usr/bin/env python3
# -*- coding: UTF-8 -*-                                                                                                                                                 
#import chardet
import socket
import os
import sys
import time
import logging
import threading
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch9
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime

# Raspberry Pi pin configuration:                                                                                                                                       
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level = logging.DEBUG)

#mirror image
def mirror_image(image):
    # Mirror the image horizontally
    mirrored_image = ImageOps.mirror(image)
    return mirrored_image

def show_on_display(text):
    try:
        disp = LCD_1inch9.LCD_1inch9()
        disp.Init()
        disp.clear()
        disp.bl_DutyCycle(50)
        Font1 = ImageFont.truetype("../Font/Font01.ttf", 25)
        image1 = Image.new("RGB", (disp.height,disp.width ), "BLACK")
        draw = ImageDraw.Draw(image1)
        draw.text((30, 30), text, fill = "WHITE", font=Font1)
        image1=mirror_image(image1)
        disp.ShowImage(image1)
        time.sleep(15)
    except IOError as e:
        logging.info(e)

def update_time_on_display():
    while True:
        # Get the current time, but only the minutes
        current_time = datetime.now().strftime("%H:%M")
        # Call the modified show_on_display function with an empty message and only time
        show_on_display(current_time)
        # Wait for 60 seconds before updating the time again
        time.sleep(60)

def start_server():
    try:
        # Server address and port
        server_address = '192.168.158.223'  # IP address to bind to (localhost)
        server_port = 65432  # Port number to listen on
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the address and port
        server_socket.bind((server_address, server_port))
        # Listen for incoming connections (max 1 connection in the queue)
        server_socket.listen(1)
        print(f"Server listening on {server_address}:{server_port}")

        # Accept a connection
        connection, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        try:
            while(1 == 1):
                # Receive the message from the client
                message = connection.recv(1024).decode('utf-8')
                print(f"Message from client: {message}")
                show_on_display(message)

                # Send a response back to the client
                response_message = "Hello, Client!"
                connection.sendall(response_message.encode('utf-8'))
                print(f"Sent response to client: {response_message}")
                time.sleep(15)

        finally:
            # Clean up the connection
            connection.close()
            print("Connection closed")
    except Exception as e:
        print(f"An error occured: {e}")

# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Start the time update function in a separate thread
time_thread = threading.Thread(target=update_time_on_display)
time_thread.start()