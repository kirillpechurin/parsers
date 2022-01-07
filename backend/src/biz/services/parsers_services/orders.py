from datetime import datetime

import pytz
from bson import ObjectId

from src.biz.services.base_service import BaseService


class OrderService(BaseService):

    def __init__(self):
        super(OrderService, self).__init__()
        self.collection = self.db_name['orders']

    def update_status_order(self, order_id: str):
        self.collection.update_one({"_id": ObjectId(order_id)}, {"$set": {"status_ready": True}})

    def create_order(self, data, email):
        order = self.collection.insert_one({
            "data": data,
            "email": email,
            "created_at": datetime.now(tz=pytz.UTC),
            "status_ready": False
        })
        return str(order.inserted_id)

    def get_by_email(self, email):
        results = self.collection.find(
            {
                "email": email,
                "status_ready": True
            }
        )
        results = [result for result in results]
        return results
