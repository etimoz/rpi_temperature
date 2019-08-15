import datetime

from django.core.management import BaseCommand

from HomeTemperature.models import TemperatureData


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('number_of_data', type=int)

    def handle(self, *args, **options):
        nr_of_data = options['number_of_data']
        for i in range(nr_of_data):
            tmp_date = datetime.datetime.now() + datetime.timedelta(hours=i)
            data = TemperatureData(temperature=i, humidity=i, date=tmp_date)
            data.save()
