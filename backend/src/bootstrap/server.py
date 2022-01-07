from fastapi import FastAPI


class Server:

    app = None

    @classmethod
    def set_app(cls, app):
        cls.app: FastAPI = app

    @classmethod
    def set_routers(cls, routers):
        cls.app: FastAPI
        for router in routers:
            cls.app.include_router(router)
