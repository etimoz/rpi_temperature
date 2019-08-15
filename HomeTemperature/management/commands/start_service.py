from django.core.management.base import BaseCommand

from HomeTemperature.temperature_service import TemperatureService


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('pin', type=int)
        parser.add_argument('minutes', type=int)

    def handle(self, *args, **options):
        pin = options['pin']
        time = options['minutes']
        print(pin)
        print(time)
        if pin and time:
            service = TemperatureService(sensor_pin=pin, minutes=time)
        else:
            service = TemperatureService()

        service.run()
