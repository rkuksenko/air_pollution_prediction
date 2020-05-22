from django.shortcuts import render
from django.http import HttpResponse
from .city import City

def index(request):
    return render(request, 'index.html', {})


def predict(request):
    return render(request, 'predict.html', {})


def handle_city(request):
    city = City(request.POST['citychoice'])

    return render(request, 'city_info.html', {'city': city.get_name()})
