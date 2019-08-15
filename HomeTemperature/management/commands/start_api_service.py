from django.core.management.base import BaseCommand

from HomeTemperature.temperature_service import TemperatureService


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)
        parser.add_argument('minutes', type=int)


    def handle(self, *args, **options):
        url = options["url"]
        minutes = options["minutes"]
        service = TemperatureService(url, minutes)
        service.run()
