from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.biz.services.auth_services.auth import AuthService
from src.biz.services.auth_services.token import JWTService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_from_token(token):
    account_id = JWTService.decode_token(token)
    account = AuthService().get_by_id(account_id=account_id)
    return account


def get_current_account(token: str = Depends(oauth2_scheme)):
    return get_from_token(token)
