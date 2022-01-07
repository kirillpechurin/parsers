from app.exception_handlers.custom import validation_exception_handler, http_exception_handler, api_exception_handler
from .custom import APIException, HTTPException, RequestValidationError


handlers = [
    (api_exception_handler, APIException),
    (http_exception_handler, HTTPException),
    (validation_exception_handler, RequestValidationError)
]
