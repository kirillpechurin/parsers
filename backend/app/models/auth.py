import datetime

from pydantic import EmailStr, BaseModel

from src.biz.services.auth_services.token import TOKEN_LIFETIME_SECONDS


class AuthRegisterData(BaseModel):
    email: EmailStr
    password: str
    repeat_password: str


class AuthLoginData(BaseModel):
    email: EmailStr
    password: str


class AuthToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = TOKEN_LIFETIME_SECONDS


class Account(BaseModel):
    account_id: str
    email: EmailStr
    first_name: str = ""
    last_name: str = ""
    confirmed: bool = False
    created_at: datetime.datetime = None

    @classmethod
    def parse_obj(cls, obj: dict):
        data = {}
        if obj.get("_id"):
            data["account_id"] = str(obj.pop("_id"))
        data.update(obj)
        return super(Account, cls).parse_obj(data)
