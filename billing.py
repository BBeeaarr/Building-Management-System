import RPi.GPIO as GPIO
import time
from threading import Thread
from threading import Lock
red_led = 22
blue_led = 18

class HVAC_BILL:
	def __init__(self,hvac):
		GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
		GPIO.setup(red_led, GPIO.OUT)    # set ledPin to OUTPUT mode
		GPIO.setup(blue_led, GPIO.OUT)
		self.hvacStatus = hvac
		self.lock = Lock()
		self.blueTime = 0
		self.redTime = 0
		t1 = Thread(target =self.monitor,daemon=True)
		t1.start()
	def update(self,hvac):
		self.hvacStatus = hvac
		
	def monitor(self):
		while(True):
			
			if(self.hvacStatus == 'COOL'):
				self.lock.acquire()
				GPIO.output(blue_led,GPIO.HIGH)
				GPIO.output(red_led,GPIO.LOW)
				self.lock.release()
				self.blueTime = self.blueTime + .1
			elif(self.hvacStatus == 'HEAT'):
				self.lock.acquire()
				GPIO.output(red_led,GPIO.HIGH)
				GPIO.output(blue_led,GPIO.LOW)
				self.lock.release()
				self.redTime = self.redTime + .1
			else:
				self.lock.acquire()
				GPIO.output(red_led,GPIO.LOW)
				GPIO.output(blue_led,GPIO.LOW)
				self.lock.release()
			time.sleep(.1)
			
	def emergencyON(self):
		#self.lock.acquire()
		GPIO.output(red_led,GPIO.HIGH)
		GPIO.output(blue_led,GPIO.HIGH)
		time.sleep(1.5)
	
	def emergencyOFF(self):
		GPIO.output(red_led,GPIO.LOW)
		GPIO.output(blue_led,GPIO.LOW)
		time.sleep(1.5)
		#self.lock.release()
	
	
		
