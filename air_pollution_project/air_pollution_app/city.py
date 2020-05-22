
class City:
    cities = {'kiev': 'Kiev',
              'krakow': 'Krakow',
              'london': 'London',
              'istanbul': 'Istanbul'}

    def __init__(self, city):
        self._city = city

    def get_name(self):
        return self.cities[self._city]

    def __str__(self):
        return self.get_name()