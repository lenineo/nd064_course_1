from flask import Flask
from flask import json
import logging
app = Flask(__name__)


@app.route("/")
def hello():
    app.logger.debug("Request Hello World")
    return "Hello World!"

@app.route("/status")
def status():
    data = {"result" : "OK - healthy"}
    response = app.response_class(
         response=json.dumps(data),
         status=200,
         mimetype='application/json'
 )
    app.logger.debug("Request /status")
    return response

@app.route("/metrics")
def metrics():
    data = {"data" : {"UserCount": 140, "UserCountActive": 23}}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
     )
    app.logger.debug("Request /metrics")
    return response

if __name__ == "__main__":
    logging.basicConfig(filename='app.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    app.run(host='0.0.0.0')

