import flask
import datetime
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

app = flask.Flask(__name__)

@app.route('/')
def index():
    humid, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    temp = temp * 1.8 + 32
    temp_str = '{0:.1f}'.format(temp) + 'F'
    humid_str = '{0:.1f}'.format(humid) + '%'
    freezer = temp_str+ '/' + humid_str
    date = str(datetime.datetime.now().strftime('%b %d %Y'))
    time = str(datetime.datetime.now().strftime('%-I:%M%p'))
    return flask.render_template('index.html', freezer=freezer, date=date, time=time)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
