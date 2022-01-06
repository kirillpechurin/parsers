from pydantic import EmailStr, BaseModel


class AuthRegisterData(BaseModel):
    email: EmailStr
    password: str
    repeat_password: str
