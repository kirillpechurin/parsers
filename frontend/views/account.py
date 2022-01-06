from flask import Blueprint, request, url_for, render_template, flash
from werkzeug.utils import redirect

from src.services.account import AccountService

account = Blueprint("account", __name__)


@account.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        repeat_password = request.form.get("repeat_password")
        data = {
            "email": email,
            "password": password,
            "repeat_password": repeat_password
        }
        response, errors = AccountService.signup(data=data)
        if errors:
            flash(errors)
            return redirect(url_for("account.signup"))
        return redirect(url_for("account.login"))
    return render_template("account/signup.html")
