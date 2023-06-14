import RPi.GPIO as GPIO
from time import sleep
from threading import Lock
from threading import Thread

buttonUp = 35 #increase temperature
buttonDown = 37 #decrease temperature


class TEMP_SETTING:
	def __init__(self,initialTemp):
		GPIO.setmode(GPIO.BOARD)        
		GPIO.setup(buttonUp, GPIO.IN,pull_up_down=GPIO.PUD_UP)    
		GPIO.setup(buttonDown, GPIO.IN,pull_up_down=GPIO.PUD_UP)  
		self.desiredTemp = initialTemp
		self.lock = Lock()
		t1 = Thread(target =self.monitor,daemon=True)
		t1.start()
		
	def incTemp(self,channel):
		self.lock.acquire()
		self.desiredTemp = self.desiredTemp + 1
		self.lock.release()
		
	def decTemp(self,channel):
		self.lock.acquire()
		self.desiredTemp = self.desiredTemp - 1
		self.lock.release()
		
	def monitor(self):
		GPIO.add_event_detect(buttonUp, GPIO.RISING,self.incTemp,100)
		GPIO.add_event_detect(buttonDown,GPIO.RISING,self.decTemp,100)
		while(True):
			sleep(.33333)
	
	
		
