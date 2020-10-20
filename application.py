import os

from app import create_app

application = create_app()
#application.config.update(SECRET_KEY=os.environ['SECRET_KEY'])

application.config.update(SECRET_KEY='test_key')

if __name__ == '__main__':
    application.run(port=9001)
