from app import app, LOGGER
from app.database import Database
from app.forms import NewItemForm
from flask import abort, request, render_template
from flask.json import jsonify

DATABASE = Database()

APPNAME = "scan2kasse"


@app.route('/')
def index():
    return "<h1>Hello, World!</h>", 200

@app.route('/test')
def test():
    if request.args:
        LOGGER.debug(request.args['testing'])
    form = NewItemForm()
    return render_template("test.html", form=form)


@app.route(f'/{APPNAME}/login')
def login():
    if not request.json or 'login' not in request.json:
        abort(400)
    if not DATABASE.get_user(login = request.json['login']):
        abort(403)
    return jsonify({}), 200


@app.route(f'/{APPNAME}/insert', methods=['POST'])
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

@app.route(f'/{APPNAME}/overview', methods=['GET'])
def get_report_from_user():
    user, month, year = []*3
    if request.args:
        args = request.args
        if 'month' in args:
            month = args['month']
        if 'year' in args:
            year = args['year']
    if month and (month > 12 or month < 1):
        abort(400)
    LOGGER.info("Getting results.")
    results = DATABASE.get_report(user=user, year=year, month=month)
    LOGGER.debug(f"Results received: {results}")
    if results:
        result_dict = group_results(results)
    else:
        result_dict = {}
    if request.content_type == "application/json":
        return jsonify(result_dict)
    else:
        return render_template("overview.html", results=result_dict)


def group_results(results: tuple) -> dict:
    result_dict = {}
    LOGGER.debug("Grouping...")
    for result in results:
        if result[0] not in result_dict:
            result_dict[result[0]] = {"sum": 0}
        if str(result[1]) not in result_dict[result[0]]:
            result_dict[result[0]][str(result[1])] = {}
        result_dict[result[0]][str(result[1])][result[2]] = (
            result[3], result[4])
        price = int(result[3]) * int(float(result[4].split(" ")[0].replace(",", "."))*100)
        result_dict[result[0]]["sum"] += price
    for key in result_dict.keys():
        result_dict[key]["sum"] /= 100
    LOGGER.debug("Grouped.")
    return result_dict