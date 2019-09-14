import time
from datetime import datetime
import csv

import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4


while True:
    now = datetime.now()

    humidity0, temperature0 = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    timestamp0 = now

#    print(temperature0, humidity0, timestamp0)

    with open('temperature.csv', 'a+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([timestamp0, temperature0, humidity0])

    now = datetime.now()
    sleep_time = 5.0 - (now.second % 5 + now.microsecond/1000000.0)
    time.sleep(sleep_time)
