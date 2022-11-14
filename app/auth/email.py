from flask import current_app
from app.utils.email import send_email
from app.utils.routes_utils import render_custom_template as render_template


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Scan2Kasse] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))