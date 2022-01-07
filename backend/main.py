from fastapi import FastAPI
from src.bootstrap.server import Server
from app.routers import api_routers
from app.exception_handlers import handlers

app = FastAPI()


def init_app():
    Server.set_app(app)
    Server.set_routers(api_routers)
    Server.set_exception_handlers(handlers)
    Server.set_static()


init_app()
