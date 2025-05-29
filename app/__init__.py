from flask import Flask

app = Flask(__name__, template_folder='templates')
app = Flask(__name__, static_folder='static', template_folder='templates')


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    from .routes import main
    app.register_blueprint(main)

    return app
