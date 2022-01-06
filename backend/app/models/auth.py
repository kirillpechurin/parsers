import datetime

from pydantic import EmailStr, BaseModel


class AuthRegisterData(BaseModel):
    email: EmailStr
    password: str
    repeat_password: str


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
