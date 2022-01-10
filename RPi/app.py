from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time as t
import datetime
import sys
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(16, GPIO.OUT)

app = Flask(__name__)


def StartBrewingCoffee():
    GPIO.output(16, GPIO.LOW)


def StopBrewingCoffee():
    GPIO.output(16, GPIO.HIGH)


class server_data():
    def __init__(self):
        self.hour = '00'
        self.minute = '00'
        self.alarm = 'checked'

    def _setAlarm(self, time):
        wakeup_time = time.strftime("%H:%M:%S")
        print('Alarm will go off '+wakeup_time)
        while True:
            t.sleep(1)
            current_time = datetime.datetime.now()
            now = current_time.strftime("%H:%M:%S")
            if now == wakeup_time:
                #GPIO.output(16, GPIO.LOW)
                print('Alarmen er startet!')
                # Wait for an hour, then turn off coffee machine
                t.sleep(3600)
                #GPIO.output(16, GPIO.HIGH)
                break

    def toggleAlarm(self, toggle):
        if toggle:
            self.alarm = 'checked'
            _time = datetime.time(int(self.hour), int(self.minute), 00)
            self.alarmThread = threading.Thread(
                target=self._setAlarm, args=[_time])
            self.alarmThread.start()
        else:
            self.alarm = ''
            try:
                self.alarmThread.join()
            except AttributeError or RuntimeError:
                pass

    def setTime(self, h, m):
        self.hour = h
        self.minute = m

    def hour(self):
        return self.hour

    def minute(self):
        return self.minute


sd = server_data()


@app.route('/')
def index():
    templateData = {
        'time_hour': sd.hour,
        'time_minute': sd.minute,
        'alarm_on': sd.alarm
    }
    return render_template('index.html', **templateData)


@app.route('/<control>/<data>')
def command(control, data):
    print('control: '+control+'\ndata: '+data)
    # It's a command
    if control == 'cmnd':
        if data == 'on':
            print('coffe started brewing')
            StartBrewingCoffee()
        if data == 'off':
            print('coffe stopped brewing')
            StopBrewingCoffee()

    if control == 'alarm':
        if sd.alarm == '':
            sd.toggleAlarm(True)
        elif sd.alarm == 'checked':
            sd.toggleAlarm(False)

        print('The alarm is: ' + sd.alarm)

    # It's a time for alarm
    if control == 'time':
        _hour, _minute = data.split('-')
        sd.setTime(_hour, _minute)
        # set alarm time - hour minute
        print(sd.hour, sd.minute)

    templateData = {
        'time_hour': sd.hour,
        'time_minute': sd.minute,
        'alarm_on': sd.alarm
    }

    return render_template('index.html', **templateData)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
