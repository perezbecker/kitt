import RPi.GPIO as GPIO
import time

class ButtonCounter:
  'Encapsulates the attributes and methods to use Kitts button'

  inputPin = 29
  ledPin = 36
  ticks = 0

  def __init__(self, inputPin, ledPin):
    self.inputPin = inputPin
    self.ledPin = ledPin   

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(29, GPIO.IN)  #HARDCODED INPUTPIN (BUTTON)
    GPIO.setup(36, GPIO.OUT) #HARDCODED LEDPIN (BLUE LED #1)
    GPIO.add_event_detect(29, GPIO.RISING, callback=self.event_callback)

  def getTicks(self):
    return self.ticks

  def resetTicks(self):
    self.ticks = 0

  def event_callback(self,channel):
    self.ticks += 1
    GPIO.output(36,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(36,GPIO.LOW)
