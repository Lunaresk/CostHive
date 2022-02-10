from app import app, LOGGER
#from app.forms import NewItemForm
from app.models import User
from flask import abort, request, render_template
from flask.json import jsonify
from app.utils import view_utils, database_utils

APPNAME = "scan2kasse"


@app.route('/')
def index():
    return "<h1>Hello, World!</h>", 200

@app.route('/test')
def test():
    if request.args:
        LOGGER.debug(request.args['testing'])
    #form = NewItemForm()
    #return render_template("test.html", form=form)


@app.route(f'/{APPNAME}/login')
def login():
    if not request.json or 'login' not in request.json:
        abort(400)
    if not User.query.get(request.json['login']):
        abort(403)
    return jsonify({}), 200


@app.route(f'/{APPNAME}/insert', methods=['POST'])
def insert():
    match request.json:
        case {'user': user, 'items': items, 'date': date}:
            failed = database_utils.insert_bought_items(user, items, date)
        case {'user': user, 'items': items}:
            failed = database_utils.insert_bought_items(user, items)
        case _:
            abort(400)
    if failed:
        return jsonify(failed), 400
    return jsonify({'inserted': True}), 201

@app.route(f'/{APPNAME}/overview', methods=['GET'])
def get_report_from_user():
    user, month, year = [None]*3
    if request.args:
        args = request.args
        if 'month' in args:
            month = int(args['month'])
        if 'year' in args:
            year = int(args['year'])
    if month and (month > 12 or month < 1):
        abort(400)
    LOGGER.info("Getting results.")
    results = database_utils.get_report(user=user, year=year, month=month)
    LOGGER.debug(f"Results received: {results}")
    if results:
        result_dict = view_utils.group_results(results)
    else:
        result_dict = {}
    if request.content_type == "application/json":
        return jsonify(result_dict)
    else:
        return render_template("overview.html", results=result_dict)