from database import Database
from flask import Flask, abort, request
from flask.json import jsonify
from gevent.pywsgi import WSGIServer
import logging


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")

fileHandler = logging.FileHandler("../logs/server.log")
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(logging.INFO)
LOGGER.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
LOGGER.addHandler(consoleHandler)

app = Flask(__name__)
DATABASE = Database()


@app.route('/')
def index():
    return "<h1>Hello, World!</h>", 200


@app.route('/scan2kasse/login')
def login():
    if not request.json or 'login' not in request.json:
        abort(400)
    if not DATABASE.get_user(login = request.json['login']):
        abort(403)
    return jsonify({}), 200


@app.route('/scan2kasse/insert', methods=['POST'])
def insert():
    match request.json:
        case {'user': user, 'items': items, 'date': date}:
            failed = DATABASE.insert_bought_items(user, items, date)
            if failed:
                return jsonify(failed), 400
            return jsonify({'inserted': True}), 201
        case {'user': user, 'items': items}:
            failed = DATABASE.insert_bought_items(user, items)
            if failed:
                return jsonify(failed), 400
            return jsonify({'inserted': True}), 201
        case _:
            abort(400)

@app.route('/scan2kasse/<string:user>', methods=['GET'])
@app.route('/scan2kasse/<int:year>/<int:month>', methods=['GET'])
@app.route('/scan2kasse/<string:user>/<int:year>', methods=['GET'])
@app.route('/scan2kasse/<string:user>/<int:year>/<int:month>', methods=['GET'])
def get_monthly_report_from_user(user: str = None, year: int = None, month: int = None):
    if month and (month > 12 or month < 1):
        abort(400)
    LOGGER.info("Getting results.")
    results = DATABASE.get_report(user=user, year=year, month=month)
    LOGGER.debug("Results get")
    if results:
        result_dict = group_results(results)
    else:
        result_dict = {}
    return jsonify(result_dict)


def group_results(results: tuple) -> dict:
    result_dict = {}
    LOGGER.debug("Grouping...")
    for result in results:
        if result[0] not in result_dict:
            result_dict[result[0]] = {}
        if result[1] not in result_dict[result[0]]:
            result_dict[result[0]][str(result[1])] = {}
        result_dict[result[0]][str(result[1])][result[2]] = (
            result[3], result[4])
    LOGGER.debug("Grouped.")
    return result_dict


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
