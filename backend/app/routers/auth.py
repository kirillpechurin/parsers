from fastapi import APIRouter, Path, Depends
from fastapi import status
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from app.dependences.auth import get_current_account
from app.models.auth import AuthRegisterData, Account, AuthLoginData, AuthToken, ForgotPasswordData, \
    AuthResetPasswordData
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


@auth_router.post(
    "/check_token",
    summary="Проверка токена",
    description="Проверка токена через поиск пользователя",
    status_code=status.HTTP_200_OK,
    response_model=WrapModel,
    response_description="Токен валидный",
    responses={
        "200": {
            "content": {
                "application/json": {
                    "example": WrapModel(data={"status": True})
                }
            }
        },
        "422": {
            "description": "",
            "content": {
                "application/json": {
                    "example": ValidationError("Authentication credentials is not valid").exc_object
                }
            }
        },
        "42201": {
            "description": "",
            "content": {
                "application/json": {
                    "example": ValidationError("Account with such id was not found").exc_object
                }
            }
        }
    }
)
async def check_token(auth_token: AuthToken):
    account_id = JWTService.decode_token(auth_token.access_token)
    AuthService().get_by_id(account_id=account_id)
    return WrapModel(data={
        "status": True
    })


@auth_router.post(
    "/confirm/{account_id}",
    summary="Подтверждение email",
    description="Подтверждение email по ссылке, отправленной на почту",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Успешно подтвержден",
    responses={
        "422": {
            "content": {
                "application/json": {
                    "example": ValidationError("Account with such id was not found").exc_object
                }
            }
        },
        "42201": {
            "content": {
                "application/json": {
                    "example": ValidationError("Already confirmed").exc_object
                }
            }
        }
    }
)
async def confirm_email(
        account_id: str = Path(...,
                               title="Account id параметр",
                               description="Account id параметр для подтверждения email. "
                                           "Это ObjectId mongodb параметр, приведенный к строке",
                               min_length=24,
                               max_length=24)
):
    account = AuthService().get_by_id(account_id)
    if account.confirmed:
        raise ValidationError("Already confirmed")
    AuthService().confirm_account(account_id=account_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@auth_router.post(
    "/password/forgot",
    summary="Забыли пароль",
    description="Отправка ссылки для сброса пароля на email",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Ссылка успешно отправлена на email",
    responses={
        "422": {
            "content": {
                "application/json": {
                    "example": ValidationError("Account with such email was not found").exc_object
                }
            }
        },
        "42201": {
            "content": {
                "application/json": {
                    "example": ValidationError("Account is not confirmed").exc_object
                }
            }
        },
    }
)
async def forgot_password(forgot_password_data: ForgotPasswordData):
    email = forgot_password_data.email
    account = AuthService().get_by_email(email)
    if not account.confirmed:
        raise ValidationError("Account is not confirmed")
    AuthService.send_forgot_link(account.account_id, account.email)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@auth_router.post(
    "/password/reset/auth",
    summary="Смена пароля для авторизованного пользователя",
    description="Смена пароля для авторизованного пользователя",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Пароль успешно обновлен",
    responses={
        "422": {
            "description": "Некоректные данные",
            "content": {
                "application/json": {
                    "example": ValidationError("Incorrect auth data").exc_object
                }
            }
        },
        "42201": {
            "description": "Пароли не совпадают",
            "content": {
                "application/json": {
                    "example": ValidationError("Passwords does not equal").exc_object
                }
            }
        },
        "42202": {
            "description": "Длина пароля меньше нужной",
            "content": {
                "application/json": {
                    "example": ValidationError("Length password might be more than 8").exc_object
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
async def auth_reset_password(
        auth_reset_password_data: AuthResetPasswordData,
        account: Account = Depends(get_current_account)
):
    AuthService().check_by_auth_data(email=account.email, password=auth_reset_password_data.old_password)
    AuthService().update_password(account_id=account.account_id,
                                  password=auth_reset_password_data.new_password,
                                  repeat_password=auth_reset_password_data.repeat_new_password)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@auth_router.post(
    "/password/reset/{account_id}",
    summary="Смена пароля по ссылке, отправленной на почту",
    description="Смена пароля по ссылке, отправленной на почту. Для неавторизованного пользователя",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Пароль успешно обновлен",
    responses={
        "422": {
            "description": "Некоректные данные",
            "content": {
                "application/json": {
                    "example": ValidationError("Incorrect Auth Data").exc_object
                }
            }
        },
        "42201": {
            "description": "Пароли не совпадают",
            "content": {
                "application/json": {
                    "example": ValidationError("Passwords does not equal").exc_object
                }
            }
        },
        "42202": {
            "description": "Длина пароля меньше нужной",
            "content": {
                "application/json": {
                    "example": ValidationError("Length password might be more than 8").exc_object
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
async def reset_password(
        auth_register_data: AuthRegisterData,
        account_id: str = Path(...)
):
    account = AuthService().get_by_email(auth_register_data.email)
    if account.account_id != account_id:
        raise ValidationError("Incorrect Auth Data")

    AuthService().update_password(account_id=account.account_id,
                                  password=auth_register_data.password,
                                  repeat_password=auth_register_data.password)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@auth_router.post(
    "/token",
    include_in_schema=False
)
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login(
        AuthLoginData(
            email=form_data.username,
            password=form_data.password
        )
    )


@auth_router.get(
    "/me",
    summary="Детальная информация о пользователе",
    description="Детальная информация о пользователе",
    status_code=status.HTTP_200_OK,
    response_description="Успешно получена детальная информация",
    response_model=WrapModel,
    responses={
        "422": {
            "description": "Некоректные данные",
            "content": {
                "application/json": {
                    "example":ValidationError("Account with such id was not found").exc_object
                }
            }
        },
        "42201": {
            "description": "Некорректный токен",
            "content": {
                "application/json": {
                    "example": ValidationError("Authentication credentials is not valid").exc_object
                }
            }
        }
    }
)
async def get_account(
        account: Account = Depends(get_current_account)
):
    return WrapModel(data=account)
