

class APIException(Exception):
    """
    Абстрактное пользовательское исключение

    От этого класса должны наследоваться все конкретные пользовательские исключения
    """
    def __init__(self, exc_object: dict):
        self.exc_object = exc_object
        self.status_code = 418


class ValidationError(APIException):
    """
    Пользовательское исключение валидации
    """
    def __init__(self, detail: str = "Validation Error"):
        self.exc_object = {
            "code": "validation_error",
            "detail": detail
        }
        self.status_code = 422


class InternalError(APIException):
    """
    Пользовательское исключение внутренней ошибки
    """
    def __init__(self):
        self.exc_object = {
            "code": "internal_error",
            "detail": "Внутренняя ошибка. Пожалуйста, попробуйте позже"
        }
        self.status_code = 500


class NotFoundError(APIException):
    """
    Пользовательское исключение, если объект не найден
    """
    def __init__(self, detail: str = "Not Found"):
        self.exc_object = {
            "code": "not_found",
            "detail": detail
        }
        self.status_code = 404
