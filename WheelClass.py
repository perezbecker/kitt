import RPi.GPIO as GPIO
import time

class WheelEncoder:
  'Encapsulates the attributes and methods to use a wheel encoder sensor'

  inputPin = 33
  ledPin = 36
  ticks = 0
  ticksPerTurn = 1.
  radius = 334.0
  Pi = 3.14159
  cmPerTick = 2. * Pi * radius

  def __init__(self, inputPin, ticksPerTurn, radius, ledPin):
    self.inputPin = inputPin
    self.ticksPerTurn = ticksPerTurn
    self.radius = radius
    self.ledPin = ledPin   

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(33, GPIO.IN)  #HARDCODED INPUTPIN (HALL SENSOR)
    GPIO.setup(36, GPIO.OUT) #HARDCODED LEDPIN (BLUE LED #1)
    GPIO.add_event_detect(33, GPIO.RISING, callback=self.event_callback)

  def getTicks(self):
    return self.ticks

  def resetTicks(self):
    self.ticks = 0

  def getTicksPerTurn(self):
    return self.ticksPerTurn

  def setTicksPerTurn(self, ticks):
    self.ticksPerTurn = ticks

  def getRadius(self):
    return self.radius

  def setRadius(self, rad):
    self.radius = rad

  def setCmPerTick(self, ticksPerTurn, radius):
    self.cmPerTick = ( 2 * Pi * radius ) / ticksPerTurn

  def getDistance(self):
    return self.ticks * self.cmPerTick

  def event_callback(self,channel):
    self.ticks += 1
    #GPIO.output(36,GPIO.HIGH)
    #time.sleep(0.1)
    #GPIO.output(36,GPIO.LOW)
