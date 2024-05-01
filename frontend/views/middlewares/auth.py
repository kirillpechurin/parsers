from functools import wraps
from flask import session, url_for
from werkzeug.utils import redirect
from src.services.account import AccountService


def authorization_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_token = session.get("x_token")
        if not auth_token:
            return redirect(url_for("account.login"))
        data, errors = AccountService.check_token(data={"access_token": auth_token})
        if errors:
            return redirect(url_for("account.login"))

        if not data.get("status"):
            return redirect(url_for("account.login"))

        resp = func(auth_token=auth_token, *args, **kwargs)
        return resp

    return wrapper
