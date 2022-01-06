from src.biz.services.base_service import BaseService


class MapReviewsService(BaseService):

    def __init__(self):
        super(MapReviewsService, self).__init__()
        self.collection = self.db_name['reviews']

    def save_reviews(self, data, html_filename, order_id):
        self.collection.insert_one(
            {
                "html_filename": html_filename,
                "data": data,
                "order_id": order_id
            }
        )

