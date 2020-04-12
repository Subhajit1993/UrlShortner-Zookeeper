import os
from flask import Flask
import config
from controller import home
from flask_sqlalchemy import SQLAlchemy
from kazoo.client import KazooClient, KazooState, KeeperState

zk = KazooClient(hosts='localhost:2181')

app = Flask(__name__)

# app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object(config.DevelopmentConfig)
db = SQLAlchemy(app)

zk.start()


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
    app.run(host="0.0.0.0", port=5000)
