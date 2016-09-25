import gps
import Adafruit_BMP.BMP085 as BMP085
import RPi.GPIO as GPIO 
import time
import WheelClass
import ButtonClass
import datetime
import os

sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)


def LedRunningA():
	GPIO.output(40,GPIO.HIGH)
	GPIO.output(38,GPIO.LOW)
	return
def LedRunningB():
	GPIO.output(40,GPIO.LOW)
	GPIO.output(38,GPIO.HIGH)
	return

def SaveRainbow():
	GPIO.output(40,GPIO.HIGH)
	GPIO.output(35,GPIO.LOW)
	GPIO.output(36,GPIO.LOW)
	time.sleep(0.1)
        GPIO.output(40,GPIO.LOW)
        GPIO.output(35,GPIO.HIGH)
        GPIO.output(36,GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(40,GPIO.LOW)
        GPIO.output(35,GPIO.LOW)
        GPIO.output(36,GPIO.HIGH)
        time.sleep(0.1)
	return



halldata = WheelClass.WheelEncoder(33,1,334,36)
buttondata = ButtonClass.ButtonCounter(29,36)

# to use Raspberry Pi board pin numbers  
GPIO.setmode(GPIO.BOARD)  
# set up GPIO output channel  
GPIO.setup(40, GPIO.OUT) #GREEN 1
GPIO.setup(38, GPIO.OUT) #GREEN 2
GPIO.setup(35, GPIO.OUT) #RED
GPIO.setup(36, GPIO.OUT) #BLUE 1
GPIO.setup(18, GPIO.OUT) #BLUE 2

#GPIO.setup(33, GPIO.IN)    # HALL EFFECT SENSOR set GPIO13 as input  


# intialize all leds low
GPIO.output(40,GPIO.LOW)
GPIO.output(38,GPIO.LOW)

GPIO.output(35,GPIO.LOW)
GPIO.output(36,GPIO.LOW)
GPIO.output(18,GPIO.LOW)


# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)


AorB=0
TicksNow = 0
Ticks1sAgo = 0
Ticks2sAgo = 0
Ticks3sAgo = 0
Ticks4sAgo = 0
Recording = 0

LedRunningA()
ButtonOff = 0

ButtonPressNow = 0
ButtonPress1sAgo = 0
ButtonPress2sAgo = 0
ButtonPress3sAgo = 0


output = open('/mnt/usb/kittlogs/'+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')+'.txt','a')

while ButtonOff == 0:
    try:
    	report = session.next()
		# Wait for a 'TPV' report and display the current time
		# To see all report data, uncomment the line below
	#print report
        if report['class'] == 'TPV':
            if (hasattr(report, 'time') and hasattr(report, 'lat') and hasattr(report, 'lon') and hasattr(report, 'alt') and hasattr(report, 'track') and hasattr(report, 'speed') and hasattr(report, 'climb')):
                
		hrdatafile = open('/mnt/usb/kittlogs/hr.txt','r')
		hrdata = hrdatafile.readline()
		hrdatafile.close()
		
		hrsplit = hrdata.split()		

		currenttime=int(time.time())
		
		if (currenttime - int(hrsplit[1]) > 10):
		    hr = 0
	            GPIO.output(35,GPIO.HIGH)	
		else:
		    hr = int(hrsplit[0])
	            GPIO.output(35,GPIO.LOW)

		print report.time, report.lat, report.lon, report.alt, report.track, report.speed, report.climb, \
		'Altitude = {0:0.2f} m'.format(sensor.read_altitude()), 'Temp = {0:0.2f} *C'.format(sensor.read_temperature()), \
		'Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()), 'Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()), \
		"HAL:", halldata.getTicks(), "BUT:", buttondata.getTicks(),"HR:", hr, "REC:", Recording


		Ticks4sAgo = Ticks3sAgo
		Ticks3sAgo = Ticks2sAgo
		Ticks2sAgo = Ticks1sAgo
		Ticks1sAgo = TicksNow
		TicksNow = halldata.getTicks()
		
		if(TicksNow-Ticks4sAgo > 0):
			Recording = 0
		
		else:
			Recording = 1
			print >> output, report.time, report.lat, report.lon, report.alt, report.track, report.speed, report.climb, \
                	'{0:0.2f}'.format(sensor.read_altitude()), '{0:0.2f}'.format(sensor.read_temperature()), \
                	'{0:0.2f}'.format(sensor.read_pressure()), '{0:0.2f}'.format(sensor.read_sealevel_pressure()), \
                	 halldata.getTicks(), buttondata.getTicks(), hr
			if AorB == 0:
				LedRunningA()
				AorB = 1
                	elif AorB ==1:
				LedRunningB()
				AorB = 0
		
		ButtonPress3sAgo = ButtonPress2sAgo
		ButtonPress2sAgo = ButtonPress1sAgo
		ButtonPress1sAgo = ButtonPressNow
		ButtonPressNow = buttondata.getTicks()

		if(ButtonPressNow - ButtonPress3sAgo > 3):
			ButtonOff = 1
			output.close()
			GPIO.output(40,GPIO.LOW)
        		GPIO.output(38,GPIO.LOW)
			for i in range(0,8):
				SaveRainbow()
			
			GPIO.output(40,GPIO.LOW)
        		GPIO.output(35,GPIO.LOW)
       			GPIO.output(36,GPIO.LOW)
			GPIO.cleanup()
			os.system("sudo shutdown now -h")
			
    except KeyError:
		output.close()
		GPIO.cleanup()  
		pass
    except KeyboardInterrupt:
		output.close()
                GPIO.output(40,GPIO.LOW)
                GPIO.output(38,GPIO.LOW)
                for i in range(0,8):
                	SaveRainbow()

                GPIO.output(40,GPIO.LOW)
                GPIO.output(35,GPIO.LOW)
                GPIO.output(36,GPIO.LOW)
                GPIO.cleanup()  
		quit()
    except StopIteration:
		output.close()
		session = None
		print "GPSD has terminated"
