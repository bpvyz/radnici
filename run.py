from app import create_app


if __name__ == '__main__':
    app = create_app()
    app.secret_key = '123'
    app.run(port=8081)