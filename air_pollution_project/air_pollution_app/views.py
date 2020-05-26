from django.shortcuts import render
from .bl.city import City
#from air_pollution_project.air_pollution_app.bl.city import City


def index(request):
    return render(request, 'index.html', {})


def predict(request):
    return render(request, 'predict.html', {})


def handle_city(request):
    city = City(request.POST['citychoice'])
    lat, lon = city.get_location()

    return render(request, 'city_info.html', {'city': city.get_name(), 'lon': lon, 'lat': lat})

