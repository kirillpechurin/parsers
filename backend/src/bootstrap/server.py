from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


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

    @classmethod
    def set_exception_handlers(cls, handlers):
        cls.app: FastAPI
        for handler, exception_class in handlers:
            cls.app.add_exception_handler(exception_class, handler)

    @classmethod
    def set_static(cls):
        cls.app.mount("/static", StaticFiles(directory="static"), name="static")
