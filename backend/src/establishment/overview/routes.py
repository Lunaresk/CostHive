from flask import abort,  request
from flask.json import jsonify
from flask_login import current_user, login_required
from . import bp
from src import LOGGER
from src.models import Establishment
from src.utils import view_utils, database_utils
from src.utils.routes_utils import render_custom_template as render_template

@bp.route('/<int:establishment_id>', methods=['GET'])
@login_required
def get_report_from_user(establishment_id):
    Establishment.query.filter_by(id=int(establishment_id)).first_or_404()
    if current_user.is_anonymous:
        abort(403)
    if 'month' in request.args:
        try:
            month = int(request.args['month'])
        except Exception as e:
            LOGGER.exception("")
            abort(400)
        else:
            if (month > 12 or month < 1):
                abort(400)
    LOGGER.info("Getting results.")
    results = database_utils.get_report(**request.args, **{"establishment": establishment_id})
    LOGGER.debug(f"Results received.")
    LOGGER.debug(str(results))
    if results:
        result_list = view_utils.group_results(results)
    else:
        result_list = []
    LOGGER.debug(result_list)
    if request.content_type == "application/json":
        return jsonify(result_list)
    else:
        return render_template("establishment/overview/overview.html", results=result_list, establishment=Establishment.query.get(int(establishment_id)))