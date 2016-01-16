import RPi.GPIO as GPIO  
import time  
# blinking function  
def blink(pin):  
        GPIO.output(pin,GPIO.HIGH)  
        time.sleep(0.3)  
        GPIO.output(pin,GPIO.LOW)  
        time.sleep(0.3)  
        return

def running():
	GPIO.output(40,GPIO.HIGH)
	GPIO.output(38,GPIO.LOW)
	time.sleep(1)
	GPIO.output(40,GPIO.LOW)
        GPIO.output(38,GPIO.HIGH)
	time.sleep(1)
	return

def quickblink():
	GPIO.output(40,GPIO.LOW)
	GPIO.output(38,GPIO.LOW)
	GPIO.output(35,GPIO.LOW)
	GPIO.output(36,GPIO.LOW)
        GPIO.output(18,GPIO.LOW)
	time.sleep(0.1)
        GPIO.output(40,GPIO.HIGH)
        GPIO.output(38,GPIO.HIGH)
        GPIO.output(35,GPIO.HIGH)
        GPIO.output(36,GPIO.HIGH)
	GPIO.output(18,GPIO.HIGH)
        time.sleep(0.1)
        return


# to use Raspberry Pi board pin numbers  
GPIO.setmode(GPIO.BOARD)  
# set up GPIO output channel  
GPIO.setup(40, GPIO.OUT) #GREEN 1
GPIO.setup(38, GPIO.OUT) #GREEN 2
GPIO.setup(35, GPIO.OUT) #RED
GPIO.setup(36, GPIO.OUT) #BLUE 1
GPIO.setup(18, GPIO.OUT) #BLUE 2
  
# intialize all leds low
GPIO.output(40,GPIO.LOW)
GPIO.output(38,GPIO.LOW)


GPIO.output(35,GPIO.LOW)
GPIO.output(36,GPIO.LOW)
GPIO.output(18,GPIO.LOW)

# blink GPIO21 50 times  
for i in range(0,1):  
        blink(40)
	blink(38)
	blink(35)
	blink(36)
	blink(18)


for i in range(0,4):
	running()

for i in range(0,20):
        quickblink()


GPIO.cleanup()   


#PIN 40, GPIO 21: Green LED 1
#PIN 38, GPIO 20: Green LED 2

#PIN 35, GPIO 19: Red LED 
#PIN 36, GPIO 16: Blue LED 1
#PIN 18, GPIO 24: Blue LED 2 


