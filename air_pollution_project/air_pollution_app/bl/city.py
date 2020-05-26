
class City:
    cities = {'kiev': {'cityname': 'Kiev', 'lat': 50.442, 'lon': 30.492},
              'krakow': {'cityname': 'Krakow'},
              'london': {'cityname': 'London'},
              'istanbul': {'cityname': 'Istanbul'}}

    def __init__(self, city):
        self._city = city

    def get_name(self):
        return City.cities[self._city]['cityname']

    def get_location(self):
        return [City.cities[self._city]['lat'], City.cities[self._city]['lon']]

    def __str__(self):
        return self.get_name()
