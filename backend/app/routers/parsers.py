from fastapi import APIRouter, Depends
from starlette import status

from app.dependences.auth import get_current_account
from src.biz.exceptions.custom import ValidationError, NotFoundError

from app.models.auth import Account
from app.models.parsers import Order, TypeParser
from app.models.responses.wrap import WrapModel
from src.biz.services.parsers_services.maps.map_service import MapService


from src.biz.services.parsers_services.maps.map_order import MapOrderService

parser_router = APIRouter(
    prefix="/parsers",
    tags=['parsers'],
    dependencies=[Depends(get_current_account)],
    responses={
        401: {
            "description": "Пользователь не авторизован",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated",
                        "code": "not_authenticated"
                    }
                }
            }
        },
        42200: {
            "description": "Неверные данные аутентификации",
            "content": {
                "application/json": {
                    "example": ValidationError("Authentication credentials is not valid").exc_object
                }
            }
        }
    }
)


@parser_router.get(
    "/available_platforms/maps",
    response_model=WrapModel,
    status_code=status.HTTP_200_OK,
    summary="Доступные площадки карт",
    description="Метод на вывод всех доступных платформ карт",
    response_description="Вывод всех доступных платформ карт",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "name": "yandex",
                                "correct": True,
                                "link": "https://yandex.ru/maps",
                                "image_link": "images/maps/yandex_maps.jpg"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def available_platforms_maps():
    data = MapService().get_available_maps()
    return WrapModel(
        data=data
    )


@parser_router.post(
    "/orders",
    response_model=WrapModel,
    status_code=status.HTTP_201_CREATED,
    summary="Создать заказ",
    description="Метод создания заказа. Запускает задачу на парсинг",
    response_description="Успешный запуск задачи",
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "status": True
                        }
                    }
                }
            }
        },
        404: {
            "description": "Тип парсера не найден",
            "content": {
                "application/json": {
                    "example": {
                        "code": "not_found",
                        "detail": "type parser not found"
                    }
                }
            }
        }
    }
)
async def make_order(order: Order, account: Account = Depends(get_current_account)):
    if order.parser.type == TypeParser.maps.value:
        status_start = MapOrderService().start_order(order, account)
        return WrapModel(data={"status": status_start})
    raise NotFoundError(detail="type parser not found")
