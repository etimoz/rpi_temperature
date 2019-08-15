import datetime

import pytz
from HomeTemperature.models import TemperatureData, APITemperatureData

from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView


from dateutil import tz

utc_tz = tz.gettz("UTC")
europe_tz = pytz.timezone('Europe/Vienna')


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=utc_tz).astimezone(tz=europe_tz)


class LineChartJSONView(BaseLineChartView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["test"] = "test"
        return context

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        temperature_data = TemperatureData.objects.all().filter(
            date__gte=datetime.datetime.now() - datetime.timedelta(days=1))
        labels = list()

        for data in temperature_data:
            my_date = data.date
            my_date = utc_to_local(my_date)
            time_label = my_date.strftime("%d %b %H:%M")
            labels.append(time_label)
        return labels

    def get_providers(self):
        """Return names of datasets."""
        return ["Temperature"]

    def get_data(self):
        """Return 3 datasets to plot."""
        temperature_data = TemperatureData.objects.all().filter(
            date__gte=datetime.datetime.now() - datetime.timedelta(days=1))
        api_temperature_data = APITemperatureData.objects.all().filter(
            date__gte=datetime.datetime.now() - datetime.timedelta(days=1))
        temps = [data.temperature for data in temperature_data]
        temps_api = [data.temperature for data in api_temperature_data]
        return [temps, temps_api]


class HumidityJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        temperature_data = TemperatureData.objects.all()  # .filter(date__gte=datetime.now() - timedelta(days=1))
        labels = list()
        for data in temperature_data:
            my_date = data.date
            my_date = utc_to_local(my_date)
            time_label = my_date.strftime("%d %b %H:%M")
            labels.append(time_label)
        return labels

    def get_providers(self):
        """Return names of datasets."""
        return ["Humidity"]

    def get_data(self):
        """Return 3 datasets to plot."""
        temperature_data = TemperatureData.objects.all()  # .filter(date__gte=datetime.now() - timedelta(days=1))
        temps = [data.humidity for data in temperature_data]
        return [temps, ]


line_chart = TemplateView.as_view(template_name='../templates/line_chart.html')
line_chart_json = LineChartJSONView.as_view()

humidity_chart = TemplateView.as_view(template_name='../templates/line_chart.html')
humidity_chart_json = HumidityJSONView.as_view()
