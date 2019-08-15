from datetime import datetime, timedelta
from django.shortcuts import render
from HomeTemperature.models import TemperatureData


def temperature_view(request):
    return render(request, "../templates/temperature_view.html", {"name": "paul"})


from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        temperature_data = TemperatureData.objects.all().filter(date__gte=datetime.now() - timedelta(days=1))
        labels = list()
        for data in temperature_data:
            time_label = data.date
            time_label.strftime("%H:%M")
            labels.append(time_label)
        return labels

    def get_providers(self):
        """Return names of datasets."""
        return ["Temperature"]

    def get_data(self):
        """Return 3 datasets to plot."""
        temperature_data = TemperatureData.objects.all().filter(date__gte=datetime.now() - timedelta(days=1))
        temps = [data.temperature for data in temperature_data]

        return [temps, ]


line_chart = TemplateView.as_view(template_name='../templates/line_chart.html')
line_chart_json = LineChartJSONView.as_view()
