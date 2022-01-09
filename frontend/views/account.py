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
    if session.get('x_token'):
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


@account.route("/reset_password/<account_id>", methods=["GET", "POST"])
def reset_password(account_id):
    if request.method == "POST":
        data = {
            "password": request.form.get("password"),
            "repeat_password": request.form.get("repeat_password"),
            "email": request.form.get("email")
        }
        _, errors = AccountService.reset_password(account_id, data=data)
        if errors:
            flash(errors)
            return render_template("account/reset_password.html")
        flash("Пароль успешно обновлен")
        return redirect(url_for("account.login"))
    return render_template("account/reset_password.html", account_id=account_id)


@account.route('/personal_office', methods=["GET", "POST"])
@authorization_required
def personal_office(auth_token):
    detail_account, errors = AccountService.get_detail(x_token=auth_token)
    if errors:
        flash(errors)
        return redirect(url_for("parsers.index"))
    return render_template("account/personal_office.html", account=detail_account)


@account.route('/personal_office/update_account', methods=['POST'])
@authorization_required
def update_account_info(auth_token):
    detail_account, errors = AccountService.get_detail(x_token=auth_token)
    if errors:
        flash(errors)
        return redirect(url_for("account.personal_office"))
    data = {
        "email": request.form.get('email'),
    }
    if request.form.get("first_name") != detail_account.get('first_name'):
        data['first_name'] = request.form.get("first_name")
    if request.form.get("last_name") != detail_account.get("last_name"):
        data['last_name'] = request.form.get("last_name")

    _, errors = AccountService.update_account(data=data, x_token=auth_token)
    if errors:
        flash(errors)
    return redirect(url_for("account.personal_office"))


@account.route('/personal_office/update_password', methods=["POST"])
@authorization_required
def reset_password_auth(auth_token):
    data = {
        'old_password': request.form.get("old_password"),
        "new_password": request.form.get("new_password"),
        "repeat_new_password": request.form.get("repeat_new_password"),
    }

    _, errors = AccountService.update_password(data=data, x_token=auth_token)
    if errors:
        flash(errors)
    return redirect(url_for("account.personal_office"))
