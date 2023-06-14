from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
from BMS_DHT import BMS_DHT
from motion import MOTION
from time import sleep
from hvacbuttons import TEMP_SETTING
from door import DOOR
import RPi.GPIO as GPIO

class BMS_lcd:
	def __init__(self,lcd):
		self.door = 'SAFE'
		self.doorChange = DOOR()
		self.light = 'OFF'
		self.hvac = 'OFF'
		self.lcd = lcd
		self.dht = BMS_DHT()
		self.motion = MOTION()
		self.temp = TEMP_SETTING(75)
		
	def default(self):
		self.emergency()
		self.doors(self.doorChange.doorStatus)
		self.lights(self.motion.status)
		self.ac()
		self.feelsLike = self.dht.read()
		self.lcd.clear()
		self.lcd.message('{0}'.format(self.temp.desiredTemp))
		self.lcd.message('/')
		self.lcd.message('{:.0f}'.format(self.feelsLike))
		self.lcd.setCursor(8,0)
		self.lcd.message('D:')
		self.lcd.message(self.door + '\n')
		self.lcd.message('H:' + self.hvac)
		self.lcd.setCursor(8,1)
		self.lcd.message('L:' + self.light)
		sleep(3)
		self.lcd.clear()
		
	def doors(self,doorChg): 
		self.emergency()
		if self.door == doorChg:
			return
		self.lcd.clear()
		if self.doorChange.doorStatus == 'OPEN':
			self.lcd.message('DOOR/WIND OPEN\nHVAC HALTED')
			self.hvac = 'OFF'
			self.door = self.doorChange.doorStatus
		else:
			self.feelsLike = self.dht.read() 
			self.lcd.message('DOOR/WIND CLOSED\nHVAC RESUME')
			if (self.dht.read() > self.temp.desiredTemp + 3):	
				self.hvac = 'COOL'
			elif (self.dht.read() < self.temp.desiredTemp - 3):
				self.hvac = 'HEAT'
			else:
				self.hvac = 'HEAT'
			self.door = self.doorChange.doorStatus
		sleep(3)
		self.lcd.clear()
		
	def lights(self,lightChg):
		self.emergency()
		if self.light == lightChg:
			return
		self.lcd.clear()	
		self.light = lightChg
		if lightChg == 'ON':
			self.lcd.message('LIGHTS ON')
		else:
			self.lcd.message('LIGHTS OFF')
		sleep(3)
		self.lcd.clear()	
	
	def ac(self):
		self.emergency()
		self.feelsLike = self.dht.read()
		if (self.door == 'OPEN'):
			return
		if (self.temp.desiredTemp < (self.feelsLike + 3)) and (self.temp.desiredTemp > (self.feelsLike -3)):
			return	
		if self.temp.desiredTemp > (self.feelsLike + 3):
			if(self.hvac == 'HEAT'):
				return
			self.lcd.message('HVAC CHANGE\nHEAT ON')
			self.hvac = 'HEAT'
		elif self.temp.desiredTemp < (self.feelsLike - 3):
			if(self.hvac == 'COOL'):
				return
			self.lcd.message('HVAC CHANGE\nAC ON')
			self.hvac = 'COOL'
		sleep(3)
		self.lcd.clear()
		
	def emergency(self): 
		self.lcd.clear()
		while(self.dht.read() > 95):
			self.lcd.clear()
			self.lcd.message('It\'s gettin \nhot in here!')
			sleep(3)
			
				
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.



def loop():
	mcp.output(3,1)
	lcd.begin(16,2)
	test = BMS_lcd(lcd) #Default door state should be closed(check sensor), AC set to 75(have hvac decide cool/heat) lights off

	
	while(True):
		test.default()
		
		
		
		
		
		

def destroy():
    lcd.clear()
    mcp.output(3,0)
    GPIO.cleanup()
    

try:
	# Create PCF8574 GPIO adapter.
	mcp = PCF8574_GPIO(PCF8574_address)
except:
	
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
#create LCD, pass in GPIO Adaptor
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == "__main__": 
	
	print("wtf does this do?\n")
	try:
		print("initiate loop protocol...\n")
		loop()
	except KeyboardInterrupt:
		print("exiting\n")
		destroy()
		
		
