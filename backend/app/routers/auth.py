from fastapi import APIRouter

from app.models.auth import AuthRegisterData, Account, AuthLoginData, AuthToken
from src.biz.services.auth_services.auth import AuthService
from src.biz.services.auth_services.token import JWTService

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


@auth_router.post('/login')
async def login(auth_login_data: AuthLoginData):
    account = AuthService().get_account(
        email=auth_login_data.email,
        password=auth_login_data.password
    )
    access_token = JWTService.create_token(account.account_id)
    return {
        "data": AuthToken(
            access_token=access_token,
            token_type="bearer"
        )
    }
