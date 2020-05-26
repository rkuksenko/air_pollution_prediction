import logging
import requests

from ..log import logger
from ..dataset_collector.base_collector import ICollector

logger = logging.getLogger('Collector')


class WeatherCollector(ICollector):
    API_URL = 'https://dark-sky.p.rapidapi.com/'
    REQUIRED_HEADERS = {
        'x-rapidapi-host': "dark-sky.p.rapidapi.com",
        'x-rapidapi-key': "1dda49107dmsh26d5eb9e450e580p128ca7jsn23856f353a02"
    }

    QUERYSTRING = {"lang": "en", "units": "auto"}

    def __init__(self):
        logger.info('WeatherCollector created')

    def get_data(self, city):
        try:
            logger.info(f'Going to get weather data for city: {city}')
            lon, lat = self._get_coordinates(city)
            full_api_url = ''.join([WeatherCollector.API_URL, lat, ',', lon])
            logger.info(f'Going to make REST API request to a {full_api_url}')
            response = requests.request("GET",
                                        full_api_url,
                                        headers=WeatherCollector.REQUIRED_HEADERS,
                                        params=WeatherCollector.QUERYSTRING)

            return response.text
        except RuntimeError as e:
            logger.error(f'WeatherCollector API request failed: {e}')
        except KeyError as e:
            logger.error(f'Failed to get coordinates for {city}: {e}')
