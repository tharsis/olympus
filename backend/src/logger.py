import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from src.constants import ENV
from src.constants import LOG_FOLDER

logger = logging.getLogger()


def dissable_logger():
    logging.getLogger('web3.RequestManager').setLevel(logging.WARNING)
    logging.getLogger('web3.providers.HTTPProvider').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)


dissable_logger()

if ENV == 'DEV':
    # Console logger
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s', '%H:%M:%S')
    level = logging.DEBUG
else:
    # Rotating file handler
    time = datetime.now().strftime('%Y_%m_%d')
    handler = RotatingFileHandler(f'{LOG_FOLDER}/my_app_{time}.log', maxBytes=20000000, backupCount=10)
    formatter = logging.Formatter('%(asctime)s,%(msecs)03d;%(levelname)s;%(message)s', '%Y-%m-%d %H:%M:%S')
    level = logging.INFO

logger.setLevel(level)
handler.setFormatter(formatter)
logger.addHandler(handler)
