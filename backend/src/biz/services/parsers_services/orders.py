from bson import ObjectId

from src.biz.services.base_service import BaseService


class OrderService(BaseService):

    def __init__(self):
        super(OrderService, self).__init__()
        self.collection = self.db_name['orders']

    def update_status_order(self, order_id: str):
        self.collection.update_one({"_id": ObjectId(order_id)}, {"$set": {"status_ready": True}})
