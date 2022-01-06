import datetime

import pytz
from pydantic import EmailStr, BaseModel, Field

from src.biz.services.auth_services.token import TOKEN_LIFETIME_SECONDS


class AuthRegisterData(BaseModel):
    email: EmailStr = Field(
        ...,
        title="E-Mail",
        description="Адрес электронной почты",
        example="example@gmail.com"
    )
    password: str = Field(
        ...,
        title="Пароль",
        description="Пароль пользователя",
        example="admin123"
    )
    repeat_password: str = Field(
        ...,
        title="Повторенный пароль",
        description="Повторенный пароль пользователя",
        example="admin123"
    )

    class Config:
        schema_extra = {
            "example": {
                "email": "example@gmail.com",
                "password": "admin123",
                "repeat_password": "admin123",
            }
        }


class AuthLoginData(BaseModel):
    email: EmailStr = Field(
        ...,
        title="E-Mail",
        description="Адрес электронной почты",
        example="example@gmail.com"
    )
    password: str = Field(
        ...,
        title="Пароль",
        description="Пароль пользователя",
        example="admin123"
    )

    class Config:
        schema_extra = {
            "example": {
                "email": "example@gmail.com",
                "password": "admin123"
            }
        }


class AuthToken(BaseModel):
    access_token: str = Field(
        ...,
        title="Json Web Token авторизации",
        description="Токен авторизации, полученный через post запрос на метод login",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.Joh1R2dYzkRvDkqv3sygm5YyK8Gi4ShZqbhK2gxcs2U"
    )
    token_type: str = Field(
        "bearer",
        title="Тип токена",
        description="Тип токена, по умолчанию 'bearer'",
        example="bearer"
    )
    expires_in: int = Field(
        TOKEN_LIFETIME_SECONDS,
        title="Время жизни токена",
        description="Ограничивает вечность токен",
        example=60*60*24
    )

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.Joh1R2dYzkRvDkqv3sygm5YyK8Gi4ShZqbhK2gxcs2U",
                "token_type": "bearer",
                "expires_in": TOKEN_LIFETIME_SECONDS
            }
        }


class Account(BaseModel):
    account_id: str = Field(
        ...,
        title="ObjectId field entity",
        description="Mongo db ObjectId-field entity",
        example="61d1badaac78f68a978289c3"
    )
    email: EmailStr = Field(
        ...,
        title="Auth user email",
        description="E-mail address user's",
        example="example@gmail.com"
    )
    first_name: str = Field(
        "",
        title="First Name User",
        description="Information about: First Name",
        example="Firstname"
    )
    last_name: str = Field(
        "",
        title="Last Name User",
        description="Information about: Last Name",
        example="Lastname"
    )
    confirmed: bool = Field(
        False,
        title="Status confirm user",
        description="Is email confirmed",
        example=True
    )
    created_at: datetime.datetime = Field(
        None,
        title="Дата создания пользователя",
        description="Дата создания пользователя",
        example=datetime.datetime.now(tz=pytz.UTC)
    )

    class Config:
        schema_extra = {
            "example": {
                "account_id": "61d1badaac78f68a978289c3",
                "email": "example@gmail.com",
                "first_name": "Firstname",
                "last_name": "Lastname",
                "confirmed": True,
                "created_at": datetime.datetime.now(tz=pytz.UTC)
            }
        }

    @classmethod
    def parse_obj(cls, obj: dict):
        data = {}
        if obj.get("_id"):
            data["account_id"] = str(obj.pop("_id"))
        data.update(obj)
        return super(Account, cls).parse_obj(data)


class ForgotPasswordData(BaseModel):
    email: EmailStr = Field(
        ...,
        title="Email user",
        description="Confirm E-mail address user",
        example="email@gmail.com"
    )

    class Config:
        schema_extra = {
            "example": {
                "email": "example@gmail.com",
            }
        }


class AuthResetPasswordData(BaseModel):
    old_password: str = Field(
        ...,
        title="Old Password",
        description="Old password authenticated user",
        example="admin12345"
    )
    new_password: str = Field(
        ...,
        title="New password",
        description="New password authenticated user",
        example="admin1234"
    )
    repeat_new_password: str = Field(
        ...,
        title="Repeat new password",
        description="Repeat new password authenticated user",
        example="admin1234"
    )

    class Config:
        schema_extra = {
            "example": {
                "old_password": "admin12345",
                "new_password": "admin1234",
                "repeat_new_password": "admin1234",
            }
        }
