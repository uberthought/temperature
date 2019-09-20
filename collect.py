import time
from datetime import datetime
import csv

DIRECTORY='/sys/bus/w1/devices/'
SENSOR0='28-0218405bd4ff'
SENSOR1='28-021840573eff'
FILENAME='w1_slave'
TRIGGER=60

def get_temperature(sensor):
    try:
        mytemp = ''
        if sensor == 0:
            sensor = SENSOR0
        else:
            sensor = SENSOR1
        f = open(DIRECTORY + sensor + '/' + FILENAME, 'r')
        line = f.readline() # read 1st line
        crc = line.rsplit(' ',1)
        crc = crc[1].replace('\n', '')
        if crc=='YES':
            line = f.readline() # read 2nd line
            mytemp = line.rsplit('t=',1)
        else:
            mytemp = 99999
        f.close()
 
        return float(mytemp[1])/1000

    except:
        return 99999


while True:
    now = datetime.now()

    temperature0 = get_temperature(0)
    temperature1 = get_temperature(1)
    timestamp0 = now

    if temperature0 != 99999 and temperature1 != 99999:
        with open('/home/pi/temperature/temperature.csv', 'a+', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([timestamp0, temperature0, temperature1])

    now = datetime.now()
    sleep_time = TRIGGER - (now.second % TRIGGER + now.microsecond/1000000.0)
    time.sleep(sleep_time)
