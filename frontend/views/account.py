from flask import Blueprint, request, url_for, render_template, flash, session
from werkzeug.utils import redirect

from src.services.account import AccountService
from views.middlewares.auth import authorization_required

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


@account.route("/logout", methods=["POST"])
@authorization_required
def logout(auth_token):
    if request.method == "POST":
        session.pop("x_token")
    return redirect(url_for("account.login"))


@account.route('/confirm_email/<account_id>', methods=["GET"])
def confirm_email(account_id):
    _, errors = AccountService.confirm_email(account_id)
    flash_message = "Аккаунт успешно подтвержден"
    if errors:
        flash_message = errors
    flash(flash_message)
    if session['x_token']:
        return redirect(url_for("account.personal_office"))
    return redirect(url_for("account.login"))


@account.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    if request.method == 'POST':
        data = {
            'email': request.form.get("email")
        }
        _, errors = AccountService.forgot_password(data=data)
        if errors:
            flash(errors)
            return render_template("account/forgot_password.html")
        flash("Ссылка успешно отправлена")
        return redirect(url_for("account.login"))
    return render_template("account/forgot_password.html")
