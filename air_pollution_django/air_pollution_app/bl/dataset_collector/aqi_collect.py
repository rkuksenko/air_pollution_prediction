import logging
import requests
import air_pollution_django.air_pollution_app.bl.logger.log
from air_pollution_django.air_pollution_app.bl.dataset_collector.icollector import ICollector
from datetime import datetime
import json
import pandas as pd


logger = logging.getLogger('Collector')


class AqiCollector(ICollector):
    API_URL = 'https://air-quality.p.rapidapi.com/history/airquality'
    AQI_DATA_JSON_FILE = f'{ICollector.DATA_FOLDER_DIR}/aqi_data.json'
    AQI_DATA_CSV_FILE = f'{ICollector.DATA_FOLDER_DIR}/aqi_data.csv'
    REQUIRED_HEADERS = {
        'x-rapidapi-host': "air-quality.p.rapidapi.com",
        'x-rapidapi-key': "1dda49107dmsh26d5eb9e450e580p128ca7jsn23856f353a02"
    }

    def __init__(self):
        logger.info('AqiCollector created')

    def _get_data(self, city):
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

    @staticmethod
    def _normalize_aqi_dataframe(data_json: json):
        data_json = data_json['data']

        # unify time format to a '%Y-%m-%d/%H:%M'
        for sample in data_json:
            t = datetime.strptime(sample['datetime'], '%Y-%m-%d:%H')
            sample['datetime'] = t.strftime('%Y-%m-%d/%H:%M')

        # remove column with names: ID, timestamp_utc, timestamp_local
        normalized_data = pd.json_normalize(data_json)
        normalized_data = normalized_data.drop(['timestamp_utc', 'timestamp_local'], axis=1)
        normalized_data = normalized_data.drop(index=0, axis=1)

        # move column with datetime to a 0 position
        data_column = normalized_data.pop('datetime')
        normalized_data.insert(0, 'datetime', data_column)

        return normalized_data

    def collect_aqi_to_csv(self, city: str):
        logger.info('Going to collect AQI data!')

        # make API request
        row_aqi_data = self._get_data(city)
        print(row_aqi_data)
        with open(AqiCollector.AQI_DATA_JSON_FILE, 'w') as f:
            f.write(row_aqi_data)
        data_json = json.loads(row_aqi_data)

        # data_json = ICollector._get_json(AqiCollector.AQI_DATA_JSON_FILE)

        # normalize json data to a dataframe
        normalized_data = self._normalize_aqi_dataframe(data_json)

        # save json into CSV file
        normalized_data.to_csv(AqiCollector.AQI_DATA_CSV_FILE, index=False)

        logger.info('AQI data saved to a aqi_data.csv')
        return normalized_data
