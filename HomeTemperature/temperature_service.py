#from service import Service
from time import sleep

import RPi.GPIO as GPIO
from HomeTemperature import dht11
#import dht11
import requests
import json
from threading import Thread

from HomeTemperature.models import TemperatureData


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

class TemperatureService:
    def __init__(self, sensor_pin=4, minutes=60):
        self.minutes = minutes
        self.instance = dht11.DHT11(pin=sensor_pin)

    def run(self):
        while True:
            self._record_data()
            sleep(self.minutes*60)

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

    def _fetch_api_data(self, url):
        temperature, humidity = None, None
        try:
            response = requests.get(url)
            json_response = json.loads(response.text)
            temperature = json_response["currently"]["temperature"]
            humidity = json_response["currently"]["humidity"]
        except Exception as e:
            print(e)
        return temperature, humidity