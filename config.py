import os

SQLALCHEMY_DATABASE_URI = os.environ.get('SUPABASE_DB_URL') or 'postgresql://cooper:cooper12@localhost:5432/skill_tracker'

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
