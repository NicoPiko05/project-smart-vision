#!/usr/bin/env python3
# -*- coding: UTF-8 -*-                                                                                                                                                 
#import chardet
import socket
import os
import sys
import time
import logging
import threading
sys.path.append(os.path.expanduser("~/Documents/project-smart-vision/raspberry/"))
from lib import LCD_1inch9
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime

#skibidi
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

def show_on_screen(text):
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
        #time.sleep(15)
    except IOError as e:
        logging.info(e)

def update_time_on_screen():
    while True:
        # Get the current time, but only the minutes
        current_time = datetime.now().strftime("%H:%M")
        # Call the modified show_on_screen function with an empty message and only time
        show_on_screen(current_time)
        # Wait for 60 seconds before updating the time again
        time.sleep(60)



show_on_screen("Hello, World!")
#time.sleep(5000)

# Start the time update function in a separate thread
time_thread = threading.Thread(target=update_time_on_screen)
time_thread.start()