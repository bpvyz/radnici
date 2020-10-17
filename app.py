from flask import Flask
from routes import radnici

# DATA_PATH = './static/'


def create_app():
    app = Flask("radnici")
    app.register_blueprint(radnici)
    return app
