from fastapi import APIRouter
from fastapi import status

from app.models.auth import AuthRegisterData, Account, AuthLoginData, AuthToken
from app.models.responses.wrap import WrapModel
from src.biz.exceptions.custom import ValidationError, InternalError
from src.biz.services.auth_services.auth import AuthService
from src.biz.services.auth_services.token import JWTService

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@auth_router.post(
    '/signup',
    summary="Регистрация",
    description="Регистрация через email и password",
    status_code=status.HTTP_201_CREATED,
    response_model=WrapModel,
    response_description="Успешная регистрация",
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": WrapModel(data=Account(account_id="account_id", email="email@example.com")).dict()
                }
            }
        },
        422: {
            "description": "Аккаунт с таким email уже существует",
            "content": {
                "application/json": {
                    "example": ValidationError("Account with this email already exists").exc_object
                }
            }
        },
        42201: {
            "description": "Пароли не равны",
            "content": {
                "application/json": {
                    "example": ValidationError("Passwords does not equal").exc_object
                }
            }
        },
        42202: {
            "description": "Длина пароля меньше нужной",
            "content": {
                "application/json": {
                    "example": ValidationError("Length password might be more than 8").exc_object
                }
            }
        },
        500: {
            "description": "Внутренняя ошибка",
            "content": {
                "application/json": {
                    "example": InternalError().exc_object
                }
            }
        }
    }
)
async def signup(auth_data: AuthRegisterData):
    account = AuthService().create_account(
        email=auth_data.email,
        password=auth_data.password,
        repeat_password=auth_data.repeat_password
    )
    return WrapModel(data=account)


@auth_router.post(
    "/login",
    summary="Вход",
    description="Вход в систему по логину и паролю",
    status_code=status.HTTP_200_OK,
    response_model=WrapModel,
    response_description="Успешный вход в систему",
    responses={
        "200": {
            "content": {
                "application/json": {
                    "example": WrapModel(data=AuthToken(access_token="token")).dict()
                }
            }
        },
        "422": {
            "description": "Некорректные данные",
            "content": {
                "application/json": {
                    "example": ValidationError("Incorrect auth data").exc_object
                }
            }
        },
        "500": {
            "description": "Внутренняя ошибка",
            "content": {
                "application/json": {
                    "example": InternalError().exc_object
                }
            }
        }
    }
)
async def login(auth_login_data: AuthLoginData):
    account = AuthService().get_account(
        email=auth_login_data.email,
        password=auth_login_data.password
    )
    access_token = JWTService.create_token(account.account_id)
    return WrapModel(data=AuthToken(
        access_token=access_token,
    ))

