import logging


formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s::%(funcName)s(%(thread)d)] %(message)s')

logger = logging.getLogger('Collector')
logger.setLevel(logging.INFO)

file_logger = logging.FileHandler(filename='../logs.log')
file_logger.setFormatter(formatter)
logger.addHandler(file_logger)

console_logger = logging.StreamHandler()
console_logger.setFormatter(formatter)
logger.addHandler(console_logger)


logger = logging.getLogger('Predictor')
logger.setLevel(logging.INFO)

file_logger = logging.FileHandler(filename='../logs.log')
file_logger.setFormatter(formatter)
logger.addHandler(file_logger)

console_logger = logging.StreamHandler()
console_logger.setFormatter(formatter)
logger.addHandler(console_logger)
