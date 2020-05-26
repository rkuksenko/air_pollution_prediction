import logging
from datetime import datetime
import air_pollution_project.air_pollution_app.bl.log.logger
from air_pollution_project.air_pollution_app.bl.dataset_collector.collect_aqi import AqiCollector
from air_pollution_project.air_pollution_app.bl.dataset_collector.collect_weather import WeatherCollector
import pandas as pd
import json


logger = logging.getLogger('Collector')


class DataCollector:
    DATA_FOLDER_DIR = '../data'

    WEATHER_DATA_JSON_FILE = f'{DATA_FOLDER_DIR}/weather_data.json'
    WEATHER_DATA_CSV_FILE = f'{DATA_FOLDER_DIR}/weather_data.csv'

    AQI_DATA_JSON_FILE = f'{DATA_FOLDER_DIR}/aqi_data.json'
    AQI_DATA_CSV_FILE = f'{DATA_FOLDER_DIR}/aqi_data.csv'

    def __init__(self):
        self.aqi_collector = AqiCollector()
        self.weather_collector = WeatherCollector()

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

    @staticmethod
    def _normalize_weather_dataframe(data_json: json):
        data_json = data_json['hourly']['data']

        # unify time format to a '%Y-%m-%d/%H:%M'
        for sample in data_json:
            sample['time'] = datetime.utcfromtimestamp(int(sample['time'])).strftime('%Y-%m-%d/%H:%M')

        # remove column with names: ID, summary, icon, precipType
        normalized_data = pd.json_normalize(data_json)
        normalized_data = normalized_data.drop(['summary', 'icon', 'precipType'], axis=1)
        normalized_data = normalized_data.drop(index=0, axis=1)   # ID

        # move column with time to a 0 position
        data_column = normalized_data.pop('time')
        normalized_data.insert(0, 'time', data_column)

        return normalized_data

    def _collect_aqi(self, city: str):
        logging.info('Going to collect AQI data!')

        # make API request
        # row_aqi_data = self.aqi_collector.get_data(city)
        # with open(DataCollector.AQI_DATA_JSON_FILE, 'w') as f:
        #     f.write(row_aqi_data)

        data_json = DataCollector._get_json(DataCollector.AQI_DATA_JSON_FILE)
        # data_json = json.loads(row_aqi_data)

        # normalize json data to a dataframe
        normalized_data = DataCollector._normalize_aqi_dataframe(data_json)

        # save json into CSV file
        normalized_data.to_csv(DataCollector.AQI_DATA_CSV_FILE, index=False)

        logging.info('AQI data saved to a aqi_data.csv')

    def _collect_weather(self, city: str):
        logging.info('Going to collect Weather data!')

        # make API request
        # row_weather_data = self.weather_collector.get_data(city)
        #
        # with open(DataCollector.WEATHER_DATA_JSON_FILE, 'w') as f:
        #     f.write(row_weather_data)

        # data_json = json.loads(row_weather_data)
        data_json = DataCollector._get_json(DataCollector.WEATHER_DATA_JSON_FILE)

        # normalize json data to a dataframe
        normalized_data = DataCollector._normalize_weather_dataframe(data_json)

        # save json into CSV file
        normalized_data.to_csv(DataCollector.WEATHER_DATA_CSV_FILE, index=False)
        logging.info('Weather data saved to a weather_data.csv')

    @staticmethod
    def _get_json(filename: str):
        try:
            data = ''
            with open(filename, 'r') as f:
                data = f.read()
            return json.loads(data)

        except PermissionError as e:
            logger.error(f'File [{e.filename}] Permission error, maybe it already opened. {e}')
        except FileNotFoundError as e:
            logger.error(f'File not found. {e}')
        except Exception as e:
            logger.error(f'Exception caught: {e}')

    def collect_all_data(self, city: str):
        try:
            self._collect_aqi(city)
            self._collect_weather(city)

        except PermissionError as e:
            logger.error(f'[{e.filename}]Permission denied, check maybe it already opened: ')
        except Exception as e:
            logger.error(f'Failed to collect data: {e}')


d = DataCollector()
d.collect_all_data('Kiev')
