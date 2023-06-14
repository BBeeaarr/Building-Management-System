import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
from threading import Lock

doorPin = 32

class DOOR:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
		GPIO.setup(doorPin, GPIO.IN,pull_up_down=GPIO.PUD_UP)    # set ledPin to OUTPUT mode
		self.doorStatus = 'SAFE'
		self.lock = Lock()
		t1 = Thread(target =self.monitor,daemon=True)
		t1.start()
		
	def changeDoor(self,channel):
		self.lock.acquire()
		if(self.doorStatus == 'SAFE'):
			self.doorStatus = 'OPEN'
			#print('door opened')
		else:
			self.doorStatus = 'SAFE'
			#print('door closed')
		self.lock.release()
	
	def monitor(self):
		GPIO.add_event_detect(doorPin, GPIO.BOTH,self.changeDoor,100)
		while(True):
			sleep(.1)
