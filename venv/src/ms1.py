from flask import Flask, jsonify
import requests
from requests import Session
import logging, os, sys

def setup_connector(app, name='default', **options):
    if not hasattr(app, 'extensions'):
        app.extensions = {}

    if 'connectors' not in app.extensions:
        app.extensions['connectors'] = {}

    session =  Session()

    if 'auth' in options:
        session.auth = options['auth']

    headers = options.get('headers', {})

    if 'Content-Type' not in headers:
        headers['Content-Type'] = 'application/json'

    session.headers.update(headers)

    app.extensions['connectors'][name] = session
    return session

def get_connector(app, name='default'):
    return app.extensions['connectors'][name]

def defineLogger(level, f):
    """
    # define a logger with 2 handlers, one to the console and other to a file
    # logging levels= CRITICAL:50, ERROR:40, WARNING:30, INFO:20, DEBUG:10, NOTSET:0
    """

    # create logger
    logger = logging.getLogger(f'{f}')
    logger.setLevel(level)

    # create console handler and set level to debug
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(level)

    # create file handler and set level to debug
    fileHandler = logging.FileHandler(filename=f'{f}.log', mode='a')
    fileHandler.setLevel(level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(funcName)s (line %(lineno)d) - %(levelname)s: %(message)s',
                                  datefmt='%d/%m/%Y %H:%M:%S')

    # add formatter to consoleHandler
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # add consoleHandler to logger
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    return logger

app = Flask(__name__)
setup_connector(app)

@app.route('/api', methods=['GET', 'POST'])
# @app.route('/api')

def my_ms1():

    logger.info("before call")

    # with get_connector(app) as conn:
    #     sub_result = conn.get('http://localhost:5000/api')

    sub_result = requests.get('http://localhost:5000/api')
    logger.info(f"result:{sub_result.text}")

    #     # value_ms0 = sub_result['from ms0']
    #
    #     # return jsonify(
    #     #     {'from ms0': 1234, 'my_ms1': 'That works, folk!'}
    #     # )
    return jsonify({'my_ms1': 'That works, folk!'})

if __name__ == '__main__':

    # create a logger and define its logging level
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(PROJECT_ROOT)
    logger = defineLogger(20, os.path.join(BASE_DIR, "log", os.path.basename(__file__)))
    logger.info('program started')

    app.run(port=5001)