#!/usr/bin/env python3
########################################################################
# Filename    : SenseLED.py
# Description : Control led with infrared Motion sensor.
# Author      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
from time import sleep

ledPin = 38       # define ledPin
sensorPin = 40    # define sensorPin

def setup():
    GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPin, GPIO.OUT)    # set ledPin to OUTPUT mode
    GPIO.setup(sensorPin, GPIO.IN)  # set sensorPin to INPUT mode

def loop():
    count = 0
    while True:
        if GPIO.input(sensorPin)==GPIO.HIGH:
            GPIO.output(ledPin,GPIO.HIGH) # turn on led
            print ('led turned on >>>')
            count = count + 1
        else :
            GPIO.output(ledPin,GPIO.LOW) # turn off led
            print ('led turned off <<<')
        sleep(1)
        print(count)

def destroy():
    GPIO.cleanup()                     # Release GPIO resource

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()

