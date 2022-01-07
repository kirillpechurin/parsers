from typing import Dict

from src.cel.tasks import map_parser_task

from app.models.auth import Account
from app.models.parsers import Order, DetailOrder, MapReviews
from src.biz.services.parsers_services.orders import OrderService

from src.biz.services.parsers_services.maps.map_reviews import MapReviewsService


class MapOrderService:

    def __init__(self):
        self.task = map_parser_task

    @staticmethod
    def __prepare_task_data(order: Order) -> Dict[str, str]:
        """
        Подготовить данные для задачи

        :param order: сущность заказа
        :return: Dict
        """
        return {
            "city": order.data.city,
            "organisation": order.data.organisation
        }

    @staticmethod
    def __create_order(order: Order, account: Account) -> str:
        """
        Создать заказ

        :param order: сущность заказа
        :param account: сущность пользователя
        :return: order id
        """
        order_data = order.dict()
        order_id = OrderService().create_order(data=order_data, email=account.email)
        return order_id

    def start_order(self, order: Order, account: Account):
        """
        Запустить заказ

        Создает заказ
        Подготавливает данные для задачи и запускает задачу
        :param order: сущность заказа
        :param account: сущность пользователя
        :return: успешно создан
        """
        order_id = self.__create_order(order, account)
        data = self.__prepare_task_data(order)
        self.task.delay(
            order.parser.name,
            data,
            order_id
        )
        return True

    @staticmethod
    def create_detail_order(order: Order, order_dict: dict) -> DetailOrder:
        """
        Создать сущность детального заказа

        :param order: сущность заказа
        :param order_dict: сущность заказа в виде order
        :return: DetailOrder
        """
        order_id = str(order_dict.get('_id'))
        review = MapReviewsService().get_by_order_id(order_id)
        return DetailOrder(
            order_id=order_id,
            data=order,
            created_at=order_dict.get("created_at"),
            result=MapReviews(
                html_filename=review.get("html_filename"),
                data=review.get("data")
            ) if review else None
        )
