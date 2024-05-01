from src.biz.services.parsers_services.orders import OrderService
from src.biz.services.parsers_services.maps.map_reviews import MapReviewsService

from ..utils import get_map_by_name, get_driver, move_file

from ..celery import app

DIRECTORY_STORAGE_MAPS_RESULT = "storage/parsers/maps/"


@app.task
def map_parser_task(map_name, data: dict, order_id: str):
    instance_class = get_map_by_name(map_name)
    driver, display = get_driver()
    reviews, html_filename, json_filename = instance_class(driver=driver, data=data).find()
    display.stop()
    OrderService().update_status_order(order_id)
    if not reviews or not html_filename:
        return "Failed parsing review from {}".format(map_name)

    new_html_filename = move_file(html_filename,
                                  DIRECTORY_STORAGE_MAPS_RESULT + html_filename.split("/")[-1],
                                  replace_on_empty="storage/")
    new_json_filename = move_file(json_filename,
                                  DIRECTORY_STORAGE_MAPS_RESULT + json_filename.split("/")[-1],
                                  replace_on_empty="storage/")

    print(new_html_filename)
    print(new_json_filename)

    MapReviewsService().save_reviews(data=reviews,
                                     html_filename=new_html_filename,
                                     order_id=order_id,
                                     json_filename=new_json_filename)

    return "Success parsing review from {}".format(map_name)
