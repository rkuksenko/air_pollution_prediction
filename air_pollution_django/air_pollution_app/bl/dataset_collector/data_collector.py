import logging
from datetime import datetime
import air_pollution_django.air_pollution_app.bl.logger.log
from air_pollution_django.air_pollution_app.bl.dataset_collector.aqi_collect import AqiCollector
from air_pollution_django.air_pollution_app.bl.dataset_collector.weather_collector import WeatherCollector
import pandas as pd
import json


logger = logging.getLogger('Collector')


class DataCollector:
    def __init__(self):
        self._aqi_collector = AqiCollector()
        self._weather_collector = WeatherCollector()
        self._dataframes = ()

    def collect_all_data(self, city: str):
        try:
            air_dataframe = self._aqi_collector.collect_aqi_to_csv(city)
            weather_dataframe = self._weather_collector.collect_weather_to_csv(city)

            self._dataframes = (air_dataframe, weather_dataframe)

        except PermissionError as e:
            logger.error(f'[{e.filename}]Permission denied, check maybe it already opened: ')
        except Exception as e:
            logger.error(f'Failed to collect data: {e}')

    def make_unique_dataframe(self):
        logger.info('Going to join all gathered data')
        result_dataframe = pd.concat([self._dataframes[0], self._dataframes[1]], axis=1, sort=False)
        logger.info(f'Result dataframe: {result_dataframe.head()}')

        result_dataframe.to_csv(f'{AqiCollector.DATA_FOLDER_DIR}/joined_data.csv', index=False)

