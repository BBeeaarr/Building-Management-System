import RPi.GPIO as GPIO
from time import sleep
from threading import Lock

buttonUp = 37 #increase temperature
buttonDown = 35 #decrease temperature


class TEMP_SETTING:
	def __init__(self,initialTemp):
		GPIO.setmode(GPIO.BOARD)        
		GPIO.setup(buttonUp, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)    
		GPIO.setup(buttonDown, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)  
		GPIO.add_event_detect(buttonUp, GPIO.RISING,self.incTemp,100)
		GPIO.add_event_detect(buttonDown,GPIO.RISING,self.decTemp,100)
		self.desiredTemp = initialTemp
		self.lock = Lock()
		
	def incTemp(self):
		self.lock.aquire()
		self.desiredTemp = self.desiredTemp + 1
		self.lock.release()
		
	def decTemp(self):
		self.lock.aquire()
		self.desiredTemp = self.desiredTemp - 1
		self.lock.relase()
		
	
		
