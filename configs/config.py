import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "MY_5€cr37_K€Y"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        (f"postgresql://{os.environ.get('DATABASE_USER', 'scan2kasse')}:{os.environ.get('DATABASE_PASS', 'asdf1337')}"
        f"@{os.environ.get('DATABASE_HOST', 'localhost')}:{os.environ.get('DATABASE_PORT', '5432')}"
        f"/{os.environ.get('DATABASE_DB', '') or os.environ.get('DATABASE_USER', 'scan2kasse')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
