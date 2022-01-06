import datetime


class Server:

    app = None

    @classmethod
    def set_secret_key(cls, secret_key):
        cls.app.secret_key = secret_key

    @classmethod
    def set_blueprints(cls, blueprints):
        for blueprint in blueprints:
            if blueprint.name == "parsers":
                cls.app.register_blueprint(blueprint, url_prefix="/")
            else:
                cls.app.register_blueprint(blueprint, url_prefix=f"/{blueprint.name}")

    @classmethod
    def set_app(cls, app):
        cls.app = app

    @classmethod
    def set_permanent_session(cls, days):
        cls.app.permanent_session_lifetime = datetime.timedelta(days=days)
