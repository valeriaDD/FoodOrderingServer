import json
import logging

import requests as requests
from flask import Flask

DINING_HALL_URL = "http://dining-hall:5001"

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route("/")
def miaw():
    return "Hello from food-ordering server"


@app.route("/miaw")
def miaw2():
    requests.post(f'{DINING_HALL_URL}/miaw', json=json.dumps('miaw'))
    return "Sent!"


if __name__ == '__main__':
    app.run(debug=True, port=5003, host="0.0.0.0")
