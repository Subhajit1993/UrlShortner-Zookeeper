import os
from flask import Flask
# import config
from controller import home
from flask_sqlalchemy import SQLAlchemy
from kazoo.client import KazooClient, KazooState, KeeperState
from flask_redis import FlaskRedis
import redis
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.getenv("ENV")
if env is None:
    env = "development"
APP_ROOT = os.path.join(os.path.dirname(__file__))  # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env.' + env)
load_dotenv(dotenv_path=dotenv_path, override=True)

app = Flask(__name__)
app.config.from_mapping(
    ENV=os.environ['ENV'],
    DEBUG=os.environ['DEBUG'],
    SQLALCHEMY_DATABASE_URI=os.environ['SQLALCHEMY_DATABASE_URI'],
    SQLALCHEMY_TRACK_MODIFICATIONS=bool(os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']),
    REDIS_URL=os.environ['REDIS_URL'],
)

print(os.environ['ZOOKEEPER_HOST'])
zk = KazooClient(hosts=os.environ['ZOOKEEPER_HOST'])
zk.start()

# app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
redis_client = redis.Redis(host=os.environ['REDIS_URL'], port=6379)


@zk.add_listener
def watch_for_ro(state):
    if state == KazooState.CONNECTED:
        if zk.client_state == KeeperState.CONNECTED_RO:
            print("Read only mode!")
        else:
            print("Read/Write mode!")


if __name__ == '__main__':
    app.add_url_rule('/', view_func=home.index)
    app.add_url_rule('/add-url', methods=['POST'], view_func=home.add_url)
    app.add_url_rule('/<short_code>', methods=['GET'], view_func=home.get_url)
    app.run(host="0.0.0.0", port="5000")
