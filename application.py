from app import create_app
import sys
import os
# import webbrowser

# application.config.update(SECRET_KEY=os.environ['SECRET_KEY'])


if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    application = create_app(template_folder=template_folder, static_folder=static_folder)
else:
    application = create_app()

application.config.update(SECRET_KEY='test_key')


if __name__ == "__main__":
  #  webbrowser.open('http://127.0.0.1:5000/')
    application.run()