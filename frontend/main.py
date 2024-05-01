import os
from flask import Flask
from src.bootstrap.server import Server
from views import blueprints

app = Flask(__name__, template_folder="templates")


def init_app():
    Server.set_app(app)
    Server.set_blueprints(blueprints)
    Server.set_secret_key(os.environ.get("SECRET_KEY"))
    Server.set_permanent_session(int(os.environ.get("PERMANENT_SESSION_DAYS")))


def run():
    Server.app.run(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    init_app()
    run()
