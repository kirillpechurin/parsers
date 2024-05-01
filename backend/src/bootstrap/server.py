from typing import List

from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


class Server:

    app = None

    @classmethod
    def set_app(cls, app):
        cls.app: FastAPI = app

    @classmethod
    def set_routers(cls, routers: List[APIRouter]):
        cls.app: FastAPI
        for router in routers:
            cls.app.include_router(router, prefix="/api/v1")

    @classmethod
    def set_exception_handlers(cls, handlers):
        cls.app: FastAPI
        for handler, exception_class in handlers:
            cls.app.add_exception_handler(exception_class, handler)

    @classmethod
    def set_static(cls):
        cls.app.mount("/static", StaticFiles(directory="static"), name="static")

    @classmethod
    def set_cors_politics(cls, origins):
        cls.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

    @classmethod
    def set_storage(cls):
        cls.app.mount("/storage", StaticFiles(directory="storage"), name="storage")
