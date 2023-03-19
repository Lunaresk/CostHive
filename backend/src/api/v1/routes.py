from src import LOGGER
from src.api import bp
from src.models.login_token import LoginToken
from src.utils import database_utils
from flask import abort, request
from flask.json import jsonify

@bp.route('/')
def token_authorization():
    LOGGER.debug("Token Login")
    if not request.json or 'login' not in request.json:
        abort(400)
    if not LoginToken.query.filter_by(token=request.json['login']).first():
        abort(403)
    return jsonify({}), 200

@bp.route('/insert_multiple_items', methods=['POST'])
def insert():
    """Accepts dictionaries in the following format:
    { 'user': <user_token>,
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
        case {'user': user, 'dates': dates}:
            failed = database_utils.insert_bought_items(user, dates)
        case _:
            abort(400)
    if failed:
        return jsonify(failed), 400
    return jsonify({'inserted': True}), 201