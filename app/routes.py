from app import app, db, LOGGER
from app.forms import NewItemForm, LoginForm
from app.models import LoginToken, User, Item, Brand, Category, PriceChange, AmountChange
from app.utils import view_utils, database_utils, routes_utils
from datetime import date
from flask import abort, flash, redirect, request, url_for
from flask.json import jsonify
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

APPNAME = "scan2kasse"

render_template = routes_utils.render_custom_template

@app.route('/')
def index():
    return "<h1>Hello, World!</h>", 200

@app.route('/test')
def test():
    if request.args:
        LOGGER.debug(request.args['testing'])
    form = NewItemForm()
    return render_template("test.html", form=form)


@app.route(f'/{APPNAME}/token_authorization')
def token_authorization():
    LOGGER.debug("Token Login")
    if not request.json or 'login' not in request.json:
        abort(400)
    if not LoginToken.query.filter_by(token=request.json['login']).first():
        abort(403)
    return jsonify({}), 200


@app.route(f'/{APPNAME}/token_insert', methods=['POST'])
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


@app.route(f'/{APPNAME}/login', methods=['GET', 'POST'])
def web_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('web_login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route(f'/{APPNAME}/newitem', methods=['GET', 'POST'])
@login_required
def new_item():
    if current_user.is_anonymous:
        abort(403)
    form=NewItemForm()
    if form.is_submitted():
        LOGGER.debug("submitted")
    if form.validate():
        LOGGER.debug("valid")
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
        return redirect(url_for('index'))
    return render_template('admin/new_item.html', form=form)

@app.route(f'/{APPNAME}/overview', methods=['GET'])
def get_report_from_user():
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
    results = database_utils.get_report(kwargs = request.args)
    LOGGER.debug(f"Results received: {results}")
    if results:
        result_list = view_utils.group_results(results)
    else:
        result_list = []
    if request.content_type == "application/json":
        return jsonify(result_list)
    else:
        return render_template("overview.html", results=result_list)