import RPi.GPIO as GPIO
import time
import datetime

#====================================================================
# Settings
#====================================================================
HEATER_PIN = 22

# number of seconds before shutting down the heater for emergency
MAX_HEATER_ON_SECONDS = 180

# init the lat time so it can start initially without a delay
heater_on_since = None
heater_is_on = False 


#====================================================================
# Turn Heater Off 
#====================================================================
def turn_off_heater():
    global heater_on_since
    global heater_is_on
 
    GPIO.output(HEATER_PIN, GPIO.HIGH)
    heater_is_on = False
    print "Heater OFF"

#====================================================================
# safty check is to check the timer to see if it's been on too long
#====================================================================
def safty_check():
    global heater_on_since
    global heater_is_on

    if (datetime.datetime.now() - heater_on_since).seconds > MAX_HEATER_ON_SECONDS:
        turn_off_heater()
        print "Heater was on for too long"


#====================================================================
# initialize GPIO
#====================================================================
GPIO.setmode(GPIO.BCM)
GPIO.setup(HEATER_PIN, GPIO.OUT)

try:
    while True:

        #safty_check()
        if GPIO.input(HEATER_PIN) == False: # Heater is ON
            print "Heater is ON"

            if not heater_is_on:
                heater_on_since = datetime.datetime.now()
                heater_is_on = True

            elif (datetime.datetime.now() - heater_on_since).seconds > MAX_HEATER_ON_SECONDS:
                GPIO.output(HEATER_PIN, GPIO.HIGH)
                heater_is_on = False
                heater_on_since = None
                print "Heater was on for too long. Safty monitor has turned off the heater"

        else:
            heater_is_on = False
            heater_on_since = None
            print "Heater is OFF"

        time.sleep(5)
except:
    # any exeption, including user shutoff, shut off the heater and exit
    GPIO.output(HEATER_PIN, GPIO.HIGH)



