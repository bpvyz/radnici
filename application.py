from app import create_app

application = create_app()

if __name__ == '__main__':
    application.secret_key = '123'
    application.run(port=9001)
