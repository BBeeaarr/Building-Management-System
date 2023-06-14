from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
from BMS_DHT import BMS_DHT

from time import sleep


class BMS_lcd:
	def __init__(self, temp,door, light, hvac, lcd):
		self.temp = temp
		self.door = door
		self.light = light
		self.hvac = hvac
		self.lcd = lcd
		self.dht = BMS_DHT()
		self.feelsLike = self.dht.read()
		print(self.dht.read())
		
	def default(self):
		self.emergency()
		self.lcd.clear()
		self.lcd.message('{0}'.format(self.temp))
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
		self.door = doorChg
		self.lcd.clear()
		if doorChg == 'OPEN':
			self.lcd.message('DOOR/WIND OPEN\nHVAC HALTED')
			self.hvac = 'OFF'
		else:
			self.lcd.message('DOOR/WIND CLOSED\nHVAC RESUME')
			if (self.dht.read() > self.temp + 3):	
				self.hvac = 'COOL'
			elif (self.dht.read() < self.temp - 3):
				self.hvac = 'HEAT'
			self.feelsLike = self.dht.read() 
		sleep(3)
		self.lcd.clear()
		
	def lights(self,lightChg):
		self.emergency()
		self.lcd.clear()
		if self.light == lightChg:
			return
		self.light = lightChg
		if lightChg == 'ON':
			self.lcd.message('LIGHTS ON')
		else:
			self.lcd.message('LIGHTS OFF')
		sleep(3)
		self.lcd.clear()	
	
	def ac(self,hvacChg): #CHANGE TO CALL TEMPERATURE SENSOR TO DETECT HEAT/AC, ADD BUTTON TO SET AC
		self.emergency()
		if (self.hvac == hvacChg):
			return
		self.lcd.clear()
		self.hvac = hvacChg
		if self.hvac == 'COOL':
			self.lcd.message('HVAC CHANGE\nAC ON')
		elif self.hvac == 'HEAT':
			self.lcd.message('HVAC CHANGE\nHEAT ON')
		else:
			self.lcd.message('HVAC CHANGE\nOFF')
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
	test = BMS_lcd(90,'SAFE','ON','COOL',lcd) #Default door state should be closed(check sensor), AC set to 75(have hvac decide cool/heat) lights off
	while(True):
		
		
		lcd.setCursor(0,0)
		lcd.cursor()
		sleep(1)
		test.default()
		test.doors('OPEN')
		test.default()
		test.doors('SAFE')
		
		
		
		
		
		

def destroy():
    lcd.clear()

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
		
		
