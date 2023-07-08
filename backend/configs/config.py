import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "s0m37h!n6-obfu5c471ng"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        (f"postgresql://{os.environ.get('DATABASE_USER', 'costhive')}:{os.environ.get('DATABASE_PASS', 'asdf1337')}"
         f"@{os.environ.get('DATABASE_HOST', 'localhost')}:{os.environ.get('DATABASE_PORT', '5432')}"
         f"/{os.environ.get('DATABASE_DB', '') or os.environ.get('DATABASE_USER', 'costhive')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['postmaster@wpgcommunity.net']
    POSTS_PER_PAGE = 15
