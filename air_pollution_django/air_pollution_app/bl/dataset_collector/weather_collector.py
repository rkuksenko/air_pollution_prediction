import logging
import requests
import json
from datetime import datetime
import pandas as pd

from air_pollution_django.air_pollution_app.bl.logger import log
from air_pollution_django.air_pollution_app.bl.dataset_collector.icollector import ICollector

logger = logging.getLogger('Collector')


class WeatherCollector(ICollector):
    API_URL = 'https://dark-sky.p.rapidapi.com/'
    WEATHER_DATA_JSON_FILE = f'{ICollector.DATA_FOLDER_DIR}/weather_data.json'
    WEATHER_DATA_CSV_FILE = f'{ICollector.DATA_FOLDER_DIR}/weather_data.csv'
    REQUIRED_HEADERS = {
        'x-rapidapi-host': "dark-sky.p.rapidapi.com",
        'x-rapidapi-key': "1dda49107dmsh26d5eb9e450e580p128ca7jsn23856f353a02"
    }

    QUERYSTRING = {"lang": "en", "units": "auto"}

    def __init__(self):
        logger.info('WeatherCollector created')

    def _get_data(self, city):
        try:
            logger.info(f'Going to get weather data for city: {city}')
            logger.info('Going to get weather data for city:')
            lon, lat = self._get_coordinates(city)
            full_api_url = ''.join([WeatherCollector.API_URL, str(lat), ',', str(lon)])
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

    @staticmethod
    def _normalize_weather_dataframe(data_json: json):
        data_json = data_json['hourly']['data']

        # unify time format to a '%Y-%m-%d/%H:%M'
        for sample in data_json:
            sample['time'] = datetime.utcfromtimestamp(int(sample['time'])).strftime('%Y-%m-%d/%H:%M')

        # remove column with names: ID, summary, icon, precipType
        normalized_data = pd.json_normalize(data_json)
        normalized_data = normalized_data.drop(['summary', 'icon', 'precipType'], axis=1)
        normalized_data = normalized_data.drop(index=0, axis=1)  # ID

        # move column with time to a 0 position
        data_column = normalized_data.pop('time')
        normalized_data.insert(0, 'time', data_column)

        return normalized_data

    def collect_weather_to_csv(self, city: str):
        logger.info('Going to collect Weather data!')

        # make API request
        raw_data = self._get_data(city)
        with open(WeatherCollector.WEATHER_DATA_JSON_FILE, 'w') as f:
            f.write(raw_data)
        data_json = json.loads(raw_data)

        # data_json = WeatherCollector._get_json(WeatherCollector.WEATHER_DATA_JSON_FILE)

        # normalize json data to a dataframe
        normalized_data = WeatherCollector._normalize_weather_dataframe(data_json)

        # save json into CSV file
        normalized_data.to_csv(WeatherCollector.WEATHER_DATA_CSV_FILE, index=False)
        logger.info('Weather data saved to a weather_data.csv')

        return normalized_data
