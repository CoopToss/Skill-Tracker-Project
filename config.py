import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cooperwashere'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SUPABASE_DB_URL') or 'postgresql://postgres.iyxtfszywwrsefhzjwzj:Tebow1215Database@aws-0-us-east-1.pooler.supabase.com:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No SUPABASE_DB_URL set for Flask application. Did you follow the setup instructions?")
