from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict', views.predict, name='predict'),
    path('CityChoice', views.handle_city, name='handle_city'),
]