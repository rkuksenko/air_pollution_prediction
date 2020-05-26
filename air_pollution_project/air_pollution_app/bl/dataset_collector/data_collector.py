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

    def _collect_aqi(self, city: str):
        logging.info('Going to collect AQI data!')
        row_aqi_data = self.aqi_collector.get_data(city)
        with open(DataCollector.AQI_DATA_JSON_FILE, 'w') as f:
            f.write(row_aqi_data)

        # data_json = DataCollector._get_json(DataCollector.AQI_DATA_JSON_FILE)

        data_json = json.loads(row_aqi_data)
        data_json = data_json['data']

        normalized_data = pd.json_normalize(data_json)
        normalized_data.to_csv(DataCollector.AQI_DATA_CSV_FILE)

        logging.info('AQI data saved to a aqi_data.csv')

    def _collect_weather(self, city: str):
        logging.info('Going to collect Weather data!')
        row_weather_data = self.weather_collector.get_data(city)

        with open(DataCollector.WEATHER_DATA_JSON_FILE, 'w') as f:
            f.write(row_weather_data)

        data_json = json.loads(row_weather_data)
        # data_json = DataCollector._get_json(DataCollector.WEATHER_DATA_JSON_FILE)

        data_json = data_json['hourly']['data']
        for sample in data_json:
            sample['time'] = datetime.utcfromtimestamp(int(sample['time'])).strftime('%Y-%m-%d %H:%M:%S')

        normalized_data = pd.json_normalize(data_json)

        normalized_data.to_csv(DataCollector.WEATHER_DATA_CSV_FILE)
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
