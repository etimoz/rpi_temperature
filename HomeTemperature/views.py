from datetime import datetime, timedelta
from django.shortcuts import render
from HomeTemperature.models import TemperatureData


def temperature_view(request):
    return render(request, "../templates/temperature_view.html", {"name": "paul"})


from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView


from dateutil import tz
local_tz = tz.tzlocal()

from datetime import datetime, timezone

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=tz.gettz("UTZ")).astimezone(tz=local_tz)

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        temperature_data = TemperatureData.objects.all()#.filter(date__gte=datetime.now() - timedelta(days=1))
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
        temperature_data = TemperatureData.objects.all()#.filter(date__gte=datetime.now() - timedelta(days=1))
        temps = [data.temperature for data in temperature_data]

        return [temps, ]
    
class HumidityJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        temperature_data = TemperatureData.objects.all()#.filter(date__gte=datetime.now() - timedelta(days=1))
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
        temperature_data = TemperatureData.objects.all()#.filter(date__gte=datetime.now() - timedelta(days=1))
        temps = [data.humidity for data in temperature_data]

        return [temps, ]


line_chart = TemplateView.as_view(template_name='../templates/line_chart.html')
line_chart_json = LineChartJSONView.as_view()



humidity_chart = TemplateView.as_view(template_name='../templates/line_chart.html')
humidity_chart_json = HumidityJSONView.as_view()
