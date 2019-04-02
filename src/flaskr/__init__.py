import os
from flask import Flask
from flask import request
from src.lib.MessagesClient import MessagesClient


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return 'Hello World!'

    @app.route('/about')
    def about():
        return 'TODO'

    @app.route('/sms', methods=['GET', 'POST'])
    def handle_sms():
        error = None
        messages_client = MessagesClient()
        if request.method == 'POST':
            print(request.data)
            return messages_client.handle_reply(request.data)
        else:
            return '200: OK'

    return app
