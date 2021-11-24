from flask import Flask
import os
from flask_cors import CORS
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

lamp = 26
GPIO.setup(lamp, GPIO.OUT)

GPIO.output(lamp, GPIO.LOW)


app = Flask(__name__)
CORS(app)

@app.route('/shutdown')
def index():
    os.system("shutdown -h now")
    return 'Shuting down'

@app.route('/lampon')
def lampon():
    GPIO.output(lamp, GPIO.LOW)
    return 'alarm on'

@app.route('/lampoff')
def lampoff():
    GPIO.output(lamp, GPIO.HIGH)
    return 'alarm off'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')