from flask import Flask
from routes import radnici
from base import session

# DATA_PATH = './static/'


def create_app():
    app = Flask("radnici")

    @app.teardown_request
    def teardown_request(exception):
        if exception:
            session.rollback()
        else:
            session.commit()

    app.register_blueprint(radnici)
    return app
