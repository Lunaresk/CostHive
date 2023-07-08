from src import LOGGER
from src.api.v1 import bp
from models.login_token import LoginToken
from src.utils import database_utils
from flask import abort, request
from flask.json import jsonify


@bp.route('/token_authorization')
def token_authorization():
    LOGGER.debug("Token Login")
    if not request.is_json or 'login' not in request.json:
        abort(400, "No JSON provided or keyword 'login' not in JSON.")
    if not LoginToken.query.filter_by(token=request.json['login']).first():
        abort(403)
    return jsonify({}), 200


@bp.route('/insert_multiple_items', methods=['POST'])
def insert():
    """Accepts dictionaries in the following format:
    { 'token': <user_token>,
      'dates': [
        { 'date': <date_of_insertion>,
          'items': [
            { 'item_id': <item_id>,
              'amount': <amount>            
            }
          ]
        }
      ]
    }
    """
    match request.json:
        case {'token': token, 'dates': dates}:
            failed = database_utils.insert_bought_items(token, dates)
        case _:
            LOGGER.debug("JSON formatted wrongly.")
            abort(400, "JSON formatted wrongly.")
    if failed:
        return jsonify(failed), 206
    return jsonify({}), 204
