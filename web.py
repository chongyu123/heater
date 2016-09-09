from flask import Flask
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

HEATER_PIN = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(HEATER_PIN, GPIO.OUT)

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


@app.route("/")
def stat():
    heater_stat = "OFF"

    if GPIO.input(HEATER_PIN) == False: # Heater is ON
        heater_stat = "ON"

    result = '''
<!DOCTYPE html>
<html>
<head>
	<meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;" />
	<meta charset="utf8" />
	<meta name="apple-mobile-web-app-capable" content="yes" />
	<meta http-equiv="Cache-control" content="no-cache" />
</head><body>
'''
    temp = "current temp: <b>{} C</b>".format(get_temp("28-00000521330e"))
    result += temp
    result += "</br>Heater is "
    result += heater_stat
    result += '''
</body></html>
'''

    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

