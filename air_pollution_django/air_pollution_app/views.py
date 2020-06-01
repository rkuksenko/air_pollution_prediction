from django.shortcuts import render
from .bl.city import CityInfo
from .models import City as CityData
from .bl.csv_to_html_convertor import CsvToHtmlWeatherConverter


def index(request):
    return render(request, 'index.html', {})


def predict(request):
    cities_list = CityData.objects.all()
    print(len(cities_list))

    return render(request, 'predict.html', {'cities_list': cities_list})


def handle_city(request):
    city = CityInfo(request.POST['citychoice'])
    lat, lon = city.get_location()

    w = CsvToHtmlWeatherConverter()
    weather = w.convert()
    print(weather)

    return render(request, 'city_info.html', {'city': city.get_name(), 'lon': lon, 'lat': lat, 'weather': weather})

