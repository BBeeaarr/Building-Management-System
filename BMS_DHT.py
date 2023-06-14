import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
from threading import Thread
#from cimis import CIMIS
DHTPin = 11
GPIO.setwarnings(False)

class BMS_DHT:
	def __init__(self):
		self.last3 = [0] * 3
		self.count = 0
		self.dht = DHT.DHT(DHTPin)
		#self.humidity = CIMIS()
		self.avgTemp = 70
		t1 = Thread(target =self.measure,daemon=True)
		t1.start()
		
	def read(self):
		#print('Temo:'+'{}'.format(self.avgTemp))
		#print('Humidity'+'{}'.format(.05*(float(self.humidity.cimis))))
		return (self.avgTemp)# + .05*float(self.humidity.cimis))
		
	def measure(self):
		while(True):
			chk = self.dht.readDHT11()
			if (chk is self.dht.DHTLIB_OK):
				if(self.count < 3):
					self.avgTemp = (self.dht.temperature*1.8) + 32
					self.last3[self.count] = (self.dht.temperature*1.8) + 32
				else:
					self.last3[self.count%3] = (self.dht.temperature*1.8) + 32
					self.avgTemp = (self.last3[(self.count - 2)%3] + self.last3[(self.count - 1)%3] + self.last3[self.count % 3])/3
				self.count += 1
				time.sleep(1)
