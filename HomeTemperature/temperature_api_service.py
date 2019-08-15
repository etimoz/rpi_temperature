from time import sleep

import requests
import json

from HomeTemperature.models import APITemperatureData


class TemperatureService:
    def __init__(self, url, minutes=60):
        self.minutes = minutes
        self.url = url

    def run(self):
        while True:
            self._record_data()
            sleep(self.minutes * 60)

    def _record_data(self):
        temperature, humidity = self._fetch_api_data(self.url)
        if temperature and humidity:
            data_point = APITemperatureData()
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