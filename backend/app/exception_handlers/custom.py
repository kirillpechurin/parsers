from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from src.biz.exceptions.custom import APIException


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """
    Обработчик пользовательских ошибок

    :param request: Request instance FastAPI
    :param exc: custom APIException
    :return: status_code and content error
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.exc_object
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Обработчик ошибок fastAPI.HTTPException

    :param request: Request instance FastAPI
    :param exc: fastAPI.HTTPException
    :return: status_code and content в нужном виде
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "code": "_".join(exc.detail.lower().split())
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Обработчик ошибок встроенной валидации

    :param request: Request instance FastAPI
    :param exc: fastAPI.exceptions.RequestValidationError
    :return: status_code and content в нужном виде
    """
    error_dict = exc.errors()[0]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": {
                "location": error_dict['loc'][0],
                "field": error_dict['loc'][1] if len(error_dict['loc']) > 1 else "",
                "message": error_dict['msg'],
                "type": error_dict["type"],
            },
            "body": exc.body
        }
    )
