#!/usr/bin/python                                                                                                                                                       
# -*- coding: UTF-8 -*-                                                                                                                                                 
#import chardet                                                                                                                                                         
import os
import sys
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch9
from PIL import Image, ImageDraw, ImageFont, ImageOps

# Raspberry Pi pin configuration:                                                                                                                                       
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level = logging.DEBUG)

def mirror_image(image):
    # Mirror the image horizontally
    mirrored_image = ImageOps.mirror(image)
    return mirrored_image

try:
    # display with hardware SPI:                                                                                                                                        
    ''' Warning!!!Don't create multiple displayer objects!!! '''
    #disp = LCD_1inch9.LCD_1inch9(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)                                                                    
    disp = LCD_1inch9.LCD_1inch9()
    # Initialize library.                                                                                                                                               
    disp.Init()
    # Clear display.                                                                                                                                                    
    disp.clear()
    #Set the backlight to 100                                                                                                                                           
    disp.bl_DutyCycle(50)

    Font1 = ImageFont.truetype("../Font/Font01.ttf", 25)
    Font2 = ImageFont.truetype("../Font/Font01.ttf", 35)
    Font3 = ImageFont.truetype("../Font/Font02.ttf", 32)

    # Create blank image for drawing.                                                                                                                                   
    image1 = Image.new("RGB", (disp.width,disp.height ), "WHITE")
    draw = ImageDraw.Draw(image1)
    
    logging.info("draw point")
    draw.rectangle((5, 10, 6, 11), fill = "BLACK")
    draw.rectangle((5, 25, 7, 27), fill = "BLACK")
    draw.rectangle((5, 40, 8, 43), fill = "BLACK")
    draw.rectangle((5, 55, 9, 59), fill = "BLACK")

    logging.info("draw rectangle")
    draw.rectangle([(20, 10), (70, 60)], fill = "WHITE", outline="BLUE")
    draw.rectangle([(85, 10), (130, 60)], fill = "BLUE")

    logging.info("draw line")
    draw.line([(20, 10), (70, 60)], fill = "RED", width = 1)
    draw.line([(70, 10), (20, 60)], fill = "RED", width = 1)
    draw.line([(110, 65), (110, 115)], fill = "RED", width = 1)
    draw.line([(85, 90), (135, 90)], fill = "RED", width = 1)

    logging.info("draw circle")
    draw.arc((85, 65, 135, 115), 0, 360, fill =(0, 255, 0))
    draw.ellipse((20, 65, 70, 115), fill = (0, 255, 0))
     
    logging.info("draw text")
    draw.rectangle([(0, 120), (140, 153)], fill = "BLUE")
    draw.text((5, 120), 'Hello world', fill = "RED", font=Font1)
    draw.rectangle([(0,155), (172, 195)], fill = "RED")
    draw.text((1, 155), 'WaveShare', fill = "WHITE", font=Font2)
    draw.text((5, 190), '1234567890', fill = "GREEN", font=Font3)
    text= u"微雪电子"
    draw.text((5, 230),text, fill = "BLUE", font=Font3)
    
    image1=mirror_image(image1)
    disp.ShowImage(image1)
    time.sleep(2)

    image2 = Image.new("RGB", (disp.height,disp.width ), "WHITE")
    draw = ImageDraw.Draw(image2)
    draw.text((70, 2), u"西风吹老洞庭波，", fill = "BLUE", font=Font3)
    draw.text((70, 42), u"一夜湘君白发多。", fill = "RED", font=Font3)
    draw.text((70, 82), u"醉后不知天在水，", fill = "GREEN", font=Font3)
    draw.text((70, 122), u"满船清梦压星河。", fill = "BLACK", font=Font3)

    image2=mirror_image(image2)
    disp.ShowImage(image2)
    time.sleep(2)

    logging.info("show image")
    ImagePath = ["../pic/LCD_1inch9_1.jpg", "../pic/LCD_1inch9_2.jpg", "../pic/LCD_1inch9_3.jpg"]
    for i in range(0, 3):
        image = Image.open(ImagePath[i])
        # image = image.rotate(0)                                                                                                                                       
        disp.ShowImage(image)
        time.sleep(2)
    disp.module_exit()
    logging.info("quit:")

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()