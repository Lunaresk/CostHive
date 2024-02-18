from datetime import date
from flask import render_template
from flask_login import current_user
from src import LOGGER


def get_base_infos():
    infos = {}
    infos['now'] = date.today()
    infos['current_user'] = current_user
    if current_user.is_authenticated:
        tokens = current_user.LoginToken.all()
        establishments = [logintoken.Establishment for logintoken in tokens]
        if establishments:
            infos['current_user_establishments'] = establishments
    return infos

def render_custom_template(*args, **kwargs):
    LOGGER.debug("Rendering template")
    return render_template(*args, **kwargs, **get_base_infos())