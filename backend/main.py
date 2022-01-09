from fastapi import FastAPI
from src.bootstrap.server import Server
from app.routers import api_routers
from app.exception_handlers import handlers

app = FastAPI(
    title="Parsers API",
    description="Documentation api parsers",
    version="1",
    contact={
        "name": "Kirill Pechurin",
        "email": "k.pechurin04@gmail.com"
    },
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
)

origins = [
    "http://localhost:5000",
    "localhost:5000"
]


def init_app():
    Server.set_app(app)
    Server.set_routers(api_routers)
    Server.set_exception_handlers(handlers)
    Server.set_cors_politics(origins)
    Server.set_static()
    Server.set_storage()


init_app()
