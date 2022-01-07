from .auth import auth_router
from .parsers import parser_router
from .handbooks import handbooks_router

api_routers = [
    auth_router,
    parser_router,
    handbooks_router
]
