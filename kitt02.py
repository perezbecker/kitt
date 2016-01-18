import gps
import Adafruit_BMP.BMP085 as BMP085
import RPi.GPIO as GPIO 
import time

sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)


def LedRunningA():
	GPIO.output(40,GPIO.HIGH)
	GPIO.output(38,GPIO.LOW)
	return
def LedRunningB():
	GPIO.output(40,GPIO.LOW)
	GPIO.output(38,GPIO.HIGH)
	return


# to use Raspberry Pi board pin numbers  
GPIO.setmode(GPIO.BOARD)  
# set up GPIO output channel  
GPIO.setup(40, GPIO.OUT) #GREEN 1
GPIO.setup(38, GPIO.OUT) #GREEN 2
GPIO.setup(35, GPIO.OUT) #RED
GPIO.setup(36, GPIO.OUT) #BLUE 1
GPIO.setup(18, GPIO.OUT) #BLUE 2

GPIO.setup(33, GPIO.IN)    # HALL EFFECT SENSOR set GPIO13 as input  


# intialize all leds low
GPIO.output(40,GPIO.LOW)
GPIO.output(38,GPIO.LOW)


GPIO.output(35,GPIO.LOW)
GPIO.output(36,GPIO.LOW)
GPIO.output(18,GPIO.LOW)

hall=0
AorB=0

# Define a threaded callback function to run in another thread when events are detected  
def my_callback(channel): 
	if GPIO.input(33):     # if port 25 == 1  
		print "Hall"
	else:                  # if port 25 != 1  
		pass  


GPIO.add_event_detect(33, GPIO.BOTH, callback=my_callback)

# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
    try:
    	report = session.next()
		# Wait for a 'TPV' report and display the current time
		# To see all report data, uncomment the line below
	#print report
        if report['class'] == 'TPV':
            if hasattr(report, 'time'):
                print report.time, report.lat, report.lon, report.alt, report.track, report.speed, report.climb, \
		'Altitude = {0:0.2f} m'.format(sensor.read_altitude()), 'Temp = {0:0.2f} *C'.format(sensor.read_temperature()), \
		'Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()), 'Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()), \
		hall
		
		if AorB == 0:
			LedRunningA()
			AorB = 1
                elif AorB ==1:
			LedRunningB()
			AorB = 0
    except KeyError:
		GPIO.cleanup()  
		pass
    except KeyboardInterrupt:
		GPIO.cleanup()  
		quit()
    except StopIteration:
		session = None
		print "GPSD has terminated"
