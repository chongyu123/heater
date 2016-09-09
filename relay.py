import RPi.GPIO as GPIO
import time

#====================================================================
# Settings
#====================================================================
HEATER_PIN = 22
IDEAL_TEMP = 3 # Celsius
TEMP_BUFFER = 2



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
      mytemp = 99999
    f.close()
 
    return int(mytemp[1])/1000
 
  except:
    return 99999


#====================================================================
# initialize GPIO
#====================================================================
GPIO.setmode(GPIO.BCM)
GPIO.setup(HEATER_PIN, GPIO.OUT)
GPIO.output(HEATER_PIN, GPIO.LOW)


while True:

    GPIO.output(HEATER_PIN, GPIO.LOW)
    print "relay ON"

    time.sleep(2)
        
    GPIO.output(HEATER_PIN, GPIO.HIGH)
    print "relay OFF"

    time.sleep(2)




