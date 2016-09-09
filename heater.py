import RPi.GPIO as GPIO
import time
import datetime

#====================================================================
# Settings
#====================================================================
HEATER_PIN = 22
IDEAL_TEMP = 3 # Celsius
# degree to wait until the heater starts
# ex) if the IDEAL_TEMP is 3 the heater starts at IDEAL_TEMP-TEMP_BUFFER
TEMP_BUFFER = 1

# max seconds heater is allowed be on
MAX_HEATER_ON_SECONDS = 60

# min seconds it must wait until the heater can be turned on
MIN_HEATER_OFF_SECONDS = 90 

# init the lat time so it can start initially without a delay
last_time_heater_was_on = datetime.datetime.now() - datetime.timedelta(seconds=MIN_HEATER_OFF_SECONDS)
heater_on_since = None
heater_is_on = False 

#==============================================================================
# get_temp in Celsius
#==============================================================================
def get_temp(id):
  try:
    mytemp = ''
    filename = 'w1_slave'
    f = open('/sys/bus/w1/devices/' + id + '/' + filename, 'r')
    line = f.readline() # read 1st line
    crc = line.rsplit(' ',1)
    crc = crc[1].replace('\n', '')
    if crc=='YES':
      line = f.readline() # read 2nd line
      mytemp = line.rsplit('t=',1)
    else:
      return 99999
    f.close()
 
    return int(mytemp[1])/1000
 
  except:
    return 99999


#====================================================================
# Turn Heater On
#====================================================================
def turn_on_heater():
    global last_time_heater_was_on
    global heater_on_since
    global heater_is_on
    # check if it was on recently
    if (datetime.datetime.now() - last_time_heater_was_on).seconds > MIN_HEATER_OFF_SECONDS:
 
        if not heater_is_on:
            heater_on_since = datetime.datetime.now()

        GPIO.output(HEATER_PIN, GPIO.LOW)
        heater_is_on = True
        print "Heater ON"
    else:
        print "Heater was on too recently"
    

#====================================================================
# Turn Heater Off
#====================================================================
def turn_off_heater():
    global last_time_heater_was_on
    global heater_on_since
    global heater_is_on
 
    if heater_is_on:
        last_time_heater_was_on = datetime.datetime.now()

    GPIO.output(HEATER_PIN, GPIO.HIGH)
    heater_is_on = False
    print "Heater OFF"

#====================================================================
# safty check is to check the timer to see if it's been on too long
#====================================================================
def safty_check():
    global last_time_heater_was_on
    global heater_on_since
    global heater_is_on

    if heater_is_on:
        if (datetime.datetime.now() - heater_on_since).seconds > MAX_HEATER_ON_SECONDS:
            turn_off_heater()
            print "Heater was on for too long"


#====================================================================
# initialize GPIO
#====================================================================
GPIO.setmode(GPIO.BCM)
GPIO.setup(HEATER_PIN, GPIO.OUT)

turn_off_heater()

try:
    while True:
        temp = get_temp("28-00000521330e")
        print temp, "C"

        if temp <= IDEAL_TEMP - TEMP_BUFFER:
            turn_on_heater()     

        if temp >= IDEAL_TEMP:
            turn_off_heater()      

        safty_check()

        time.sleep(5)
except:
    # any exeption, including user shutoff, shut off the heater and exit
    GPIO.output(HEATER_PIN, GPIO.HIGH)





