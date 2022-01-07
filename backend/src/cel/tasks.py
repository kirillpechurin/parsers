import os
from typing import Union

from celery import Celery

from src.biz.services.parsers_services.orders import OrderService
from src.biz.services.parsers_services.maps.map_reviews import MapReviewsService

from .utils import get_map_by_name, get_driver
from src.biz.services.mail.sender import MailService

app = Celery("tasks", backend='rpc://', broker="amqp://guest:guest@rabbitmq:5672//")
DIRECTORY_STORAGE_MAPS_RESULT = "storage/parsers/maps/"


@app.task
def map_parser_task(map_name, data: dict, order_id: str):
    instance_class = get_map_by_name(map_name)
    driver, display = get_driver()
    reviews, html_filename = instance_class(driver=driver, data=data).find()
    display.stop()
    if not reviews or not html_filename:
        return "Failed parsing review from {}".format(map_name)

    OrderService().update_status_order(order_id)
    new_html_filename = DIRECTORY_STORAGE_MAPS_RESULT + html_filename.split("/")[-1]
    os.replace(html_filename, new_html_filename)

    MapReviewsService().save_reviews(data=reviews, html_filename=new_html_filename, order_id=order_id)

    return "Success parsing review from {}".format(map_name)


@app.task
def send_on_email(to_email: str, subject: str, body: Union[list, str]):
    MailService.send(
        to=to_email,
        subject=subject,
        contents=[body] if isinstance(body, str) else body
    )
    return "Success send on email"
