import logging
import abc
import json
import air_pollution_django.air_pollution_app.bl.logger.log
from air_pollution_django.air_pollution_app.bl.city import CityInfo
from django.db import DataError, Error


logger = logging.getLogger('Collector')


class ICollector(metaclass=abc.ABCMeta):
    DATA_FOLDER_DIR = 'air_pollution_app/bl/data/'

    @staticmethod
    def _get_coordinates(city: str):
        """
        extract coordinates from database
        :return tuple {'lon': val, 'lat': val}
        """
        try:
            city = CityInfo(city)
            return city.get_location()
        except DataError as e:
            logger.error(f'DataError: {e}')
        except Error as e:
            logger.error(f'Error: {e}')


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
