from service import Service
from time import sleep
from HomeTemperature.models import TemperatureData

import RPi.GPIO as GPIO
import dht11
import schedule

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class TemperatureService(Service):
    def __init__(self, sensor_pin=4, minutes=60):
        super().__init__(self)
        self.probe_interval = minutes
        schedule.every(minutes).minutes.do(self._record_data)
        self.instance = dht11.DHT11(pin=sensor_pin)

    def run(self):
        while not self.got_sigterm():
            schedule.run_pending()
            sleep(1)

    def _capture_data(self):
        temperature, humidity = None, None
        try:
            result = self.instance.read()
            if result.is_valid():
                temperature = result.temperature
                humidity = result.humidity
                return temperature, humidity
            else:
                print("Error: %d" % result.error_code)
        except Exception as e:
            print("Failed to read data" + str(e))
        return temperature, humidity

    def _record_data(self):
        temperature, humidity = self._capture_data()
        if temperature and humidity:
            data_point = TemperatureData()
            data_point.temperature = temperature
            data_point.humidity = humidity
            data_point.save()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        sys.exit('Syntax: %s COMMAND' % sys.argv[0])

    cmd = sys.argv[1].lower()
    if sys.argv[2] and sys.argv[3]:
        pin = int(sys.argv[2].lower())
        time = int(sys.argv[3].lower())
        service = TemperatureService(sensor_pin=pin, minutes=time)
    else:
        service = TemperatureService()

    if cmd == 'start':
        service.start()
    elif cmd == 'stop':
        GPIO.cleanup()
        service.stop()
    elif cmd == 'status':
        if service.is_running():
            print("Service is running.")

        else:
            print("Service is not running.")
    else:
        GPIO.cleanup()
        sys.exit('Unknown command "%s".' % cmd)
