from fastapi import FastAPI


class Server:

    app = None

    @classmethod
    def set_app(cls, app):
        cls.app: FastAPI = app
