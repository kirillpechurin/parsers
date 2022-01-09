from datetime import datetime
from typing import Dict, List, Optional

import pymongo
import pytz
from bson import ObjectId
from pydantic import EmailStr
from src.biz.services.base_service import BaseService
from src.biz.exceptions.custom import NotFoundError

from src.biz.exceptions.enums import ExceptionEnum


class OrderService(BaseService):

    def __init__(self):
        super(OrderService, self).__init__()
        self.collection = self.db_name['orders']

    def update_status_order(self, order_id: str) -> None:
        """
        Обновить статус заказа

        :param order_id: Id заказа
        :return: None
        """
        self.collection.update_one({"_id": ObjectId(order_id)}, {"$set": {"status_ready": True}})

    def create_order(self, data: Dict, email: EmailStr) -> str:
        """
        Создать заказ

        :param data: объект Order в виде словаря
        :param email: email пользователя
        :return: order_id
        """
        order = self.collection.insert_one({
            "data": data,
            "email": email,
            "created_at": datetime.now(tz=pytz.UTC),
            "status_ready": False
        })
        return str(order.inserted_id)

    def get_by_email(self, email: EmailStr) -> List[Dict]:
        """
        Получить заказ по email

        :param email: email пользователя
        :return: Список результатов
        """
        results = self.collection.find(
            {
                "email": email,
                "status_ready": True
            }
        ).sort('created_at', pymongo.DESCENDING)
        results = [result for result in results]
        return results

    def delete_by_id(self, order_id: str) -> bool:
        """
        Удалить заказ по id

        :param order_id: Order id
        :return: Успешное удаление
        """
        self.get_by_id(order_id)
        self.collection.delete_one({"_id": ObjectId(order_id)})
        return True

    def get_by_id(self, order_id: str) -> Optional[Dict]:
        """
        Получить заказ по id

        :param order_id: Order id
        :return: dict or raise error
        """
        order = self.collection.find_one({"_id": ObjectId(order_id)})
        if not order:
            raise NotFoundError(ExceptionEnum.order_not_found)
        return order
