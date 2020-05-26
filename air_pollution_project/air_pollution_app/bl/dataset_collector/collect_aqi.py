import logging
import requests
import air_pollution_project.air_pollution_app.bl.log.logger
from air_pollution_project.air_pollution_app.bl.dataset_collector.base_collector import ICollector


logger = logging.getLogger('Collector')


class AqiCollector(ICollector):
    API_URL = 'https://air-quality.p.rapidapi.com/history/airquality'
    REQUIRED_HEADERS = {
        'x-rapidapi-host': "air-quality.p.rapidapi.com",
        'x-rapidapi-key': "1dda49107dmsh26d5eb9e450e580p128ca7jsn23856f353a02"
    }

    def __init__(self):
        logger.info('AqiCollector created')

    def get_data(self, city):
        try:
            logger.info(f'Going to get AQI data for city: {city}')
            lon, lat = self._get_coordinates(city)

            response = requests.request("GET",
                                        AqiCollector.API_URL,
                                        headers=AqiCollector.REQUIRED_HEADERS,
                                        params={"lon": lon, "lat": lat})
            return response.text
        except RuntimeError as e:
            logger.error(f'Air Quality Index API request failed: {e}')
        except KeyError as e:
            logger.error(f'Failed to get coordinates for {city}: {e}')
