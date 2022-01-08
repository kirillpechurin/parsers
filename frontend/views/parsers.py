from flask import Blueprint, request, render_template, flash, url_for
from werkzeug.utils import redirect

from src.services.handbooks import HandbookService
from src.services.parsers import ParserService
from views.middlewares.auth import authorization_required

parsers = Blueprint("parsers", __name__)


@parsers.route("/")
@authorization_required
def index(auth_token):
    return render_template("parsers/index.html")


@parsers.route('/order')
@authorization_required
def make_order(auth_token):
    data, errors = ParserService.get_available_platforms(auth_token)
    if errors:
        flash(errors)
        return redirect(url_for("parsers.index"))
    maps = data['maps']
    return render_template("parsers/make_order.html", maps=maps)


@parsers.route("/order/maps/<map_name>", methods=["GET", "POST"])
@authorization_required
def make_order_maps(auth_token, map_name):
    if request.method == "POST":
        form = request.form
        data = {
            "data": {
                "city": form.get("city"),
                "organisation": form.get("organisation"),
            },
            "parser": {
                "name": map_name,
                "type": "maps",
            }
        }
        data, errors = ParserService.make_order(data=data, x_token=auth_token)
        if errors:
            flash(errors)
            return render_template("parsers/make_order_maps.html", map_name=map_name)

        if data.get("status"):
            flash_message = "Заказ успешно создан.\n Уведомим, как только будет готово"
        else:
            flash_message = 'Ошибка при создании заказа.'
        flash(flash_message)
        return redirect(url_for("parsers.index"))
    cities, errors = HandbookService.get_cities()
    if errors:
        flash(errors)
        return redirect(url_for("parsers.index"))
    return render_template("parsers/make_order_maps.html", map_name=map_name, cities=cities)


@parsers.route('/orders', methods=["GET"])
@authorization_required
def orders(auth_token):
    response, errors = ParserService.get_orders(x_token=auth_token)
    if errors:
        flash(errors)
        return redirect(url_for("parsers.index"))
    return render_template("parsers/orders.html", orders=response)


@parsers.route("/orders/<order_id>", methods=["GET"])
@authorization_required
def order_detail(auth_token, order_id):
    response, errors = ParserService.get_detail_by_id(order_id, x_token=auth_token)
    if errors:
        flash(errors)
        return redirect(url_for("parsers.index"))
    return render_template("parsers/detail_order.html", order=response)
