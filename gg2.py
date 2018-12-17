#from _future_ import print_function
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import RPi.GPIO as GPIO

def mapObjectPosition (x, y):
    print ("[INFO] Object Center coordenates at X0 = {0} and Y0 =  {1}".format(x, y))



# initialize GPIOs
#redLed = 21
#panPin = 27
#tiltPin = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setup(redLed, GPIO.OUT)

GPIO_TRIGGER2 = 20
GPIO_ECHO2 = 16

GPIO.setup(GPIO_TRIGGER2,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO2,GPIO.IN)

#GPIO.setup(17, GPIO.OUT)
#GPIO.setup(22, GPIO.OUT)

#GPIO.setup(23, GPIO.OUT)
#GPIO.setup(24, GPIO.OUT)

def sonar(GPIO_TRIGGER,GPIO_ECHO):
      start=0
      stop=0
      # Set pins as output and input
      GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
      GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
     
      # Set trigger to False (Low)
      GPIO.output(GPIO_TRIGGER, False)
     
      # Allow module to settle
      time.sleep(0.01)
           
      #while distance > 5:
      #Send 10us pulse to trigger
      GPIO.output(GPIO_TRIGGER, True)
      time.sleep(0.00001)
      GPIO.output(GPIO_TRIGGER, False)
      begin = time.time()
      while GPIO.input(GPIO_ECHO)==0 and time.time()<begin+0.05:
            start = time.time()
     
      while GPIO.input(GPIO_ECHO)==1 and time.time()<begin+0.1:
            stop = time.time()
     
      # Calculate pulse length
      elapsed = stop-start
      # Distance pulse travelled in that time is time
      # multiplied by the speed of sound (cm/s)
      distance = elapsed * 34000
     
      # That was the distance there and back so halve the value
      distance = distance / 2
     
      print("Distance : %.1f" % distance)
      # Reset GPIO settings
      return distance





def init():
 #GPIO.setmode(GPIO.BCM)
 GPIO.setup(17, GPIO.OUT)
 GPIO.setup(22, GPIO.OUT)
 GPIO.setup(23, GPIO.OUT)
 GPIO.setup(24, GPIO.OUT)


def forward():
      init()
      GPIO.output(17, True)
      GPIO.output(22, False)
      GPIO.output(23, True)
      GPIO.output(24, False)
     
def reverse():
      GPIO.output(17, False)
      GPIO.output(22, True)
      GPIO.output(23, False)
      GPIO.output(24, True)
     
def rightturn():
      init()
      GPIO.output(17, True)
      GPIO.output(22, False)
      GPIO.output(23, False)
      GPIO.output(24, False)
     
def leftturn():
      init()
      GPIO.output(17, False)
      GPIO.output(22, False)
      GPIO.output(23, True)
      GPIO.output(24, False)

def sto():
      init()
      GPIO.output(17, False)
      GPIO.output(22, False)
      GPIO.output(23, False)
      GPIO.output(24, False)



# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] waiting for camera to warmup...")
vs = VideoStream(0).start()
time.sleep(2.0)

# define the lower and upper boundaries of the object
# to be tracked in the HSV color space
#colorLower = (24, 100, 100)
#colorUpper = (44, 255, 255)

colorLower = (110, 50, 50)
colorUpper = (139, 255, 255)


# Start with LED off
#GPIO.output(redLed, GPIO.LOW)
#ledOn = False

# Initialize servos at 90-90 position
global panServoAngle
panServoAngle = 90
global tiltServoAngle
tiltServoAngle =90

# positioning servos
print("\n Positioning servos to initial position ==> Press 'q' to quit Program \n")

# Position servos to capture object at center of screen
def servoPosition (x, y):
    distance = sonar(GPIO_TRIGGER2,GPIO_ECHO2)
    #global panServoAngle
    #global tiltServoAngle
    #if (x < 220):
        #panServoAngle += 10
        #if panServoAngle > 140:
         #   panServoAngle = 140
        #os.system("python angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
  
    #if (x > 280):
        #panServoAngle -= 10
        #if panServoAngle < 40:
         #   panServoAngle = 40
        #os.system("python angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))

    if (x < 160):
        rightturn()
        time.sleep(0.1)
        sto()
        time.sleep(0.0125)
       # forward()
       # time.sleep(0.00625)
       # sto()
       # time.sleep(0.0125)
       # rightturn()
       # time.sleep(0.00625)
        #sto()
        #time.sleep(0.0125)

        #GPIO.cleanup()
        #tiltServoAngle += 10
        #if tiltServoAngle > 140:
        #    tiltServoAngle = 140
        #os.system("python angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))
  
    elif (x > 380):
        leftturn()
        time.sleep(0.1)
        sto()
        time.sleep(0.0125)
        #forward()
        #time.sleep(0.00625)
        #sto()
        #time.sleep(0.0125)
        #leftturn()
        #time.sleep(0.00625)
        #sto()
        #time.sleep(0.0125)
        #GPIO.cleanup()
        #tiltServoAngle -= 10
        #if tiltServoAngle < 40:
        #    tiltServoAngle = 40
        #os.system("python angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))
    elif (x < 380 and x > 230):
        if (distance > 25):
           forward()
           time.sleep(0.1)
        elif (distance < 25 and distance > 22):
           reverse()
           time.sleep(0.1)  
    else:
        sto()
        time.sleep(0.01)
# loop over the frames from the video stream
while True:
	# grab the next frame from the video stream, Invert 180o, resize the
	# frame, and convert it to the HSV color space
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	frame = imutils.rotate(frame, angle=180)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the object color, then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the object
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			#distance = sonar(GPIO_TRIGGER2,GPIO_ECHO2)
			servoPosition(int(x), int(y)) 
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
                        
                        # position Servo at center of circle
			mapObjectPosition(int(x), int(y))

 
			# if the led is not already on, turn the LED on
			#if not ledOn:
			#	GPIO.output(redLed, GPIO.HIGH)
			#	ledOn = True

	# if the ball is not detected, turn the LED off
	#elif ledOn:
	#	GPIO.output(redLed, GPIO.LOW)
	#	ledOn = False

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# do a bit of cleanup
print("\n Exiting Program and cleanup stuff \n")
GPIO.cleanup()
cv2.destroyAllWindows()
vs.stop()
