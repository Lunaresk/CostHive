from app import db, LOGGER
from app.main.forms import NewItemForm
from app.main import bp
from app.models import AmountChange, Brand, Establishment, LoginToken, Item, PriceChange
from app.utils import view_utils, database_utils
from app.utils.routes_utils import render_custom_template as render_template
from datetime import date
from flask import abort, redirect, request, url_for
from flask.json import jsonify
from flask_login import current_user, login_required

@bp.route('/')
@bp.route('/index')
def index():
    return render_template("base.html")

# @bp.route('/')
# def test():
#     return "Hello World"

@bp.route('/overview', methods=['GET'])
@login_required
def get_report_from_user():
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
    results = database_utils.get_report(**request.args)
    LOGGER.debug(f"Results received.")
    # LOGGER.debug(str(results))
    if results:
        result_list = view_utils.group_results(results)
    else:
        result_list = []
    if request.content_type == "application/json":
        return jsonify(result_list)
    else:
        if "establishment" in request.args:
            return render_template("main/overview.html", results=result_list, establishment = Establishment.query.get(int(request.args['establishment'])))
        else:
            return render_template("main/overview.html", results=result_list)

@bp.route('/token_authorization')
def token_authorization():
    LOGGER.debug("Token Login")
    if not request.json or 'login' not in request.json:
        LOGGER.debug("JSON not delivered or 'login' not in JSON")
        abort(400)
    if not LoginToken.query.filter_by(token=request.json['login']).first():
        LOGGER.debug(f"Token <{request.json['login']}> not recognized")
        abort(403)
    LOGGER.debug("Token accepted")
    return jsonify({}), 200

@bp.route('/token_insert', methods=['POST'])
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

@bp.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    if current_user.is_anonymous:
        abort(403)
    form=NewItemForm.new()
    if form.is_submitted():
        LOGGER.debug("submitted")
    if form.validate():
        LOGGER.debug("valid")
    else:
        LOGGER.debug(form.errors)
    if form.validate_on_submit():
        LOGGER.debug("valid form")
        brand = Brand.query.get(form.brand.data)
        new_item = Item(id = form.id.data, name = form.name.data, brand = brand.id, description = form.description.data)
        # if form.category.data:
        #     category = Category.query.get(id = form.category.data)
        #     new_item.Category = category
        new_item.PriceChange = [PriceChange(Item = new_item, date = date(2021, 12, 1), price = form.price_change.data)]
        if form.amount_change.data:
            new_item.AmountChange = [AmountChange(Item = new_item, date = date(2021, 12, 1), amount = form.amount_change.data)]
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/new_item.html', form=form)

@bp.route('/overview/register_boughts', methods=['GET'])
@login_required
def check_unregistered_items():
    if current_user.is_anonymous or not request.args or 'establishment' not in request.args:
        abort(403)
    establishment = Establishment.query.get(int(request.args['establishment']))
    if current_user.id != establishment.owner:
        abort(403)
    results = database_utils.get_unregistered_and_register(establishment.id)
    if results:
        result_list = view_utils.group_results(results)
    else:
        result_list = []
    if request.content_type == "application/json":
        return jsonify(result_list)
    else:
        return render_template("main/overview.html", results=result_list)