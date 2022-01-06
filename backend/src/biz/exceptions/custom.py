

class APIException(Exception):

    def __init__(self, exc_object: dict):
        self.exc_object = exc_object
        self.status_code = 418


class ValidationError(APIException):

    def __init__(self, detail: str = "Validation Error"):
        self.exc_object = {
            "code": "validation_error",
            "detail": detail
        }
        self.status_code = 422


class InternalError(APIException):

    def __init__(self):
        self.exc_object = {
            "code": "internal_error",
            "detail": "internal error. Please, try again later"
        }
        self.status_code = 500
