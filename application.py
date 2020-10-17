import os

from app import create_app

application = create_app()

if __name__ == '__main__':
    application.secret_key = os.environ['SECRET_KEY']
    application.run(port=9001)
