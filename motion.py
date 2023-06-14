import RPi.GPIO as GPIO
from time import sleep

ledPin = 38       # define ledPin
sensorPin = 40    # define sensorPin

class MOTION:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
		GPIO.setup(ledPin, GPIO.OUT)    # set ledPin to OUTPUT mode
		GPIO.setup(sensorPin, GPIO.IN)  # set sensorPin to INPUT mode
		GPIO.add_event_detect(sensorPin, GPIO.BOTH,self.lightChg,100)
		self.status = 'OFF'
		
	def lightChg(self,channel):
		if self.status == 'OFF':
			self.status = 'ON'
			GPIO.output(ledPin,GPIO.HIGH)
		else:
			self.status = 'OFF'
			GPIO.output(ledPin,GPIO.LOW)
