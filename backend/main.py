from fastapi import FastAPI

from src.bootstrap.server import Server

app = FastAPI()


def init_app():
    Server.set_app(app)


init_app()
