from fastapi import APIRouter

from app.models.auth import AuthRegisterData, Account
from src.biz.services.auth_services.auth import AuthService

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@auth_router.post('/signup')
async def signup(auth_data: AuthRegisterData):
    account = AuthService().create_account(
        email=auth_data.email,
        password=auth_data.password,
        repeat_password=auth_data.repeat_password
    )
    return {
        "data": account
    }
