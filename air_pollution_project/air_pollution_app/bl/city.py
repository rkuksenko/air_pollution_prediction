from ..models import City as CityData


class City:
    # cities = {'kiev': {'cityname': 'Kiev', 'lat': 50.442, 'lon': 30.492},
    #           'krakow': {'cityname': 'Krakow', 'lat': 50.056, 'lon': 19.933},
    #           'london': {'cityname': 'London', 'lat': 51.515, 'lon': -0.154},
    #           'istanbul': {'cityname': 'Istanbul', 'lat': 41.019, 'lon': 28.946}}

    def __init__(self, city):
        self._city = city

    def get_name(self):
        c = CityData.objects.get(alias_name=self._city)
        return c.name

    def get_location(self):
        c = CityData.objects.get(alias_name=self._city)
        return c.latitude, c.longitude

    def __str__(self):
        return self.get_name()
