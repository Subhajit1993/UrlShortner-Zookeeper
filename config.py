import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.getenv("ENV")
if env is None:
    env = "development"
APP_ROOT = os.path.join(os.path.dirname(__file__))  # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env.' + env)
load_dotenv(dotenv_path, override=True)

basedir = os.path.abspath(os.path.dirname(__file__))

print( os.environ['ENV'])
class Config(object):
    ENV = os.environ['ENV']
    DEBUG = False
    TESTING = True
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']

