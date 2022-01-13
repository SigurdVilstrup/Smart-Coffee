from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time as t
from crontab import CronTab

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(16, GPIO.OUT)

app = Flask(__name__)


def StartBrewingCoffee():
    GPIO.output(16, GPIO.LOW)
    pass


def StopBrewingCoffee():
    GPIO.output(16, GPIO.HIGH)
    pass


class server_data():
    def __init__(self):
        self.hour = '00'
        self.minute = '00'
        self.alarm = ''

        # Remove all old cronjobs
        cron = CronTab(user='root')
        for job in cron:
            print(job)
        cron.remove_all()
        # And add one cronjob, start disabled
        job = cron.new(command='python /home/pi/beginCoffee.py',
                       comment='coffeeAlarm')
        job.enable(False)
        cron.write()
        for job in cron:
            print(job)

    def _setAlarm(self):
        print('Alarm will go off ')
        # Start cronjob at time ->
        cron = CronTab(user='root')
        for job in cron:
            if job.comment == 'coffeeAlarm':
                job.minute.on(int(self.minute))
                job.hour.on(int(self.hour))
                job.enable()
                cron.write()

    def _disableAlarm(self):
        cron = CronTab(user='root')
        for job in cron:
            if job.comment == 'coffeeAlarm':
                job.enable(False)
                cron.write()

    def toggleAlarm(self, toggle):
        if toggle:
            self.alarm = 'checked'
            self._setAlarm()
        elif not toggle:
            self.alarm = ''
            self._disableAlarm()

    def setTime(self, h, m):
        self.hour = h
        self.minute = m
        if self.alarm == 'checked':
            cron = CronTab(user='root')
            for job in cron:
                if job.comment == 'coffeeAlarm':
                    job.minute.on(int(self.minute))
                    job.hour.on(int(self.hour))
                    job.enable()
                    cron.write()


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
            print('coffee started brewing')
            StartBrewingCoffee()
        if data == 'off':
            print('coffee stopped brewing')
            StopBrewingCoffee()
    elif control == 'alarm':
        if data == 'true':
            sd.toggleAlarm(True)
        elif data == 'false':
            sd.toggleAlarm(False)
        pass
    elif control == 'time':
        _hour, _minute = data.split('-')
        sd.setTime(_hour, _minute)
        print(sd.hour, sd.minute)

    templateData = {
        'time_hour': sd.hour,
        'time_minute': sd.minute,
        'alarm_on': sd.alarm
    }

    return render_template('index.html', **templateData)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
