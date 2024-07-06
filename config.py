import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SUPABASE_DB_URL = os.environ.get('SUPABASE_DB_URL')
    if not SUPABASE_DB_URL:
        raise ValueError("No SUPABASE_DB_URL set for Flask application. Did you follow the setup instructions?")
    SQLALCHEMY_DATABASE_URI = SUPABASE_DB_URL
