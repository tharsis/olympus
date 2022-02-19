import os

ENV = os.getenv('ENV', 'DEV')
LOG_FOLDER = os.getenv('LOG_FOLDER', '/tmp')
REST_ENDPOINT = os.getenv('REST_ENDPOINT', 'http://1317.evmos.me/')
