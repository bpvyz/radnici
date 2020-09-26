from flask import Flask
from routes import radnici


app = Flask(__name__)
data_path = './static/'

def create_app():
    app.register_blueprint(radnici)
    return app
