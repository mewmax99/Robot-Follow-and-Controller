import RPi.GPIO as GPIO
import time

def init():
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(17, GPIO.OUT)
 GPIO.setup(22, GPIO.OUT)
 GPIO.setup(23, GPIO.OUT)
 GPIO.setup(24, GPIO.OUT)

def forward(sec):
 init()
 GPIO.output(17, True)
 GPIO.output(22, False)
 GPIO.output(23, False) 
 GPIO.output(24, False)
 time.sleep(sec)
 GPIO.cleanup()

def reverse(sec):
 init()
 gpio.output(17, False)
 gpio.output(22, True)
 gpio.output(23, False) 
 gpio.output(24, True)
 time.sleep(sec)
 gpio.cleanup()

def right(sec):
 init()
 gpio.output(18, gpio.LOW)
 gpio.output(22, gpio.HIGH)
 gpio.output(21, gpio.HIGH)
 gpio.output(19, gpio.LOW)
 time.sleep(sec)
 gpio.cleanup()


def test2(sec):
 init()
# gpio.output(17, gpio.LOW)
 gpio.output(22, gpio.HIGH)
 #gpio.output(23, gpio.HIGH)
 #gpio.output(24, gpio.LOW)
 time.sleep(sec)
 gpio.cleanup()



print("forward")
forward(4)
#print("reverse")
#reverse(2)
#right(4)
