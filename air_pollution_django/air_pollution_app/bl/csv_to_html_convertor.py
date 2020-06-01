import logging
from .logger import log


logger = logging.getLogger('Collector')


class CsvToHtmlWeatherConverter:
    DATA_FILE_PATH = 'air_pollution_app/bl/data/weather_data.csv'

    def __init__(self):
        logger.info('CsvToHtmlWeatherConverter created')

    @staticmethod
    def convert():
        try:
            raw_data = ''
            with open(CsvToHtmlWeatherConverter.DATA_FILE_PATH, 'r') as f:
                raw_data = f.readlines()

            html = []
            for row in raw_data:
                html.append(f' <p>{row.split(",")}</p>')

            res = '     '.join(html)
            return res

        except FileNotFoundError as e:
            logger.error(f'Failed to open file: [{e.filename}]')
        except Exception as e:
            logger.error(f'Error: {e}')
