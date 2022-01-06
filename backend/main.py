from fastapi import FastAPI

from src.bootstrap.server import Server
from app.routers import api_routers

app = FastAPI()


def init_app():
    Server.set_app(app)
    Server.set_routers(api_routers)


init_app()
