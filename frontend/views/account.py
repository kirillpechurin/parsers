from flask import Blueprint, request, url_for, render_template, flash, session
from werkzeug.utils import redirect

from src.services.account import AccountService

account = Blueprint("account", __name__)


@account.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = {
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "repeat_password": request.form.get("repeat_password")
        }
        response, errors = AccountService.signup(data=data)
        if errors:
            flash(errors)
            return redirect(url_for("account.signup"))
        return redirect(url_for("account.login"))
    return render_template("account/signup.html")


@account.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        data = {
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }
        response, errors = AccountService.login(data=data)
        if errors:
            flash(errors)
            return redirect(url_for("account.login"))

        session['x_token'] = response['access_token']
        return redirect(url_for("parsers.index"))

    return render_template("account/login.html")
