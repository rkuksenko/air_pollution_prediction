from ..models import City


class CityLocalTest:
    cities = {'kiev': {'cityname': 'Kiev', 'lat': 50.442, 'lon': 30.492},
              'krakow': {'cityname': 'Krakow', 'lat': 50.056, 'lon': 19.933},
              'london': {'cityname': 'London', 'lat': 51.515, 'lon': -0.154},
              'istanbul': {'cityname': 'Istanbul', 'lat': 41.019, 'lon': 28.946}}


class CityInfo:
    def __init__(self, city):
        self._city = city

    def get_name(self):
        c = City.objects.get(alias_name=self._city)
        return c.name
        # return 'Kiev'

    def get_location(self):
        c = City.objects.get(alias_name=self._city)
        return c.latitude, c.longitude
        # return [30.492, 50.442]

    def __str__(self):
        return self.get_name()
