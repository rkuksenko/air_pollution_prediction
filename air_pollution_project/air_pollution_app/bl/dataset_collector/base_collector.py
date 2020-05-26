import logging
import abc
import air_pollution_project.air_pollution_app.bl.log.logger


logger = logging.getLogger('Collector')


class ICollector(metaclass=abc.ABCMeta):
    LOCATIONS = {'Kiev': ['30.492', '50.442']}

    def _get_coordinates(self, city: str):
        """:return tuple {'lon': val, 'lat': val}"""
        city_longitude = ICollector.LOCATIONS[city][0]
        city_latitude = ICollector.LOCATIONS[city][1]
        return [city_longitude, city_latitude]

    def get_data(self, city: str):
        """ :return json object with collected data"""
        pass
