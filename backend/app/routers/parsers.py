from fastapi import APIRouter, Depends, Path
from fastapi.responses import Response
from starlette import status
from app.dependences.auth import get_current_account
from src.biz.exceptions.custom import ValidationError, NotFoundError
from app.models.auth import Account
from app.models.parsers import Order, TypeParser
from app.models.responses.wrap import WrapModel
from src.biz.services.parsers_services.maps.map_service import MapService
from src.biz.services.parsers_services.maps.map_order import MapOrderService
from src.biz.services.parsers_services.orders import OrderService
from src.biz.exceptions.enums import ExceptionEnum


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
                    "example": ValidationError(ExceptionEnum.authentication_credentials_is_not_valid).exc_object
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
        },
        404: {
            "description": "Карты не найдены",
            "content": {
                "application/json": {
                    "example": NotFoundError(ExceptionEnum.maps_not_found).exc_object
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
                    "example": NotFoundError(ExceptionEnum.type_parser_not_found).exc_object
                }
            }
        }
    }
)
async def make_order(order: Order, account: Account = Depends(get_current_account)):
    if order.parser.type == TypeParser.maps.value:
        status_start = MapOrderService().start_order(order, account)
        return WrapModel(data={"status": status_start})
    raise NotFoundError(detail=ExceptionEnum.type_parser_not_found)


@parser_router.get(
    "/orders",
    response_model=WrapModel,
    status_code=status.HTTP_200_OK,
    summary="Посмотреть все заказы",
    description="Посмотреть все созданные выполненные заказы",
    response_description="Вывод всех заказов",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": "order_id",
                                "data": {"city": "city", "organisation": "organisation"},
                                "created_at": "created_at",
                                "result": {
                                    "html_filename": "html_filename",
                                    "data": [
                                        {'address': [{}]}
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        },
        404: {
            "description": "Тип парсера не найден",
            "content": {
                "application/json": {
                    "example": NotFoundError(ExceptionEnum.type_parser_not_found).exc_object
                }
            }
        }
    }
)
async def orders(account: Account = Depends(get_current_account)):
    user_orders = OrderService().get_by_email(account.email)
    data = []
    for order in user_orders:
        order_model = Order.parse_obj(order.get("data"))
        if order_model.parser.type == TypeParser.maps.value:
            detail_order_model = MapOrderService.create_detail_order(order_model, order)
            data.append(detail_order_model)
        raise NotFoundError(ExceptionEnum.type_parser_not_found)
    return WrapModel(
        data=data
    )


@parser_router.get(
    "/orders/{order_id}",
    response_model=WrapModel,
    status_code=status.HTTP_200_OK,
    summary="Детальная информация по заказу",
    description="Детальная информация по заказу по id",
    response_description="Вывод детальной информации по заказу",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "id": "order_id",
                            "data": {"city": "city", "organisation": "organisation"},
                            "created_at": "created_at",
                            "result": {
                                "html_filename": "html_filename",
                                "data": [
                                    {'address': [{}]}
                                ]
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Order Id отсутствует",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "location": "path",
                            "field": "order_id",
                            "message": "field required",
                            "type": "type",
                        },
                        "body": {}
                    }
                }
            }
        },
        404: {
            "description": "Заказ с таким id не найден",
            "content": {
                "application/json": {
                    "example": NotFoundError(ExceptionEnum.order_not_found).exc_object
                }
            }
        },
        40401: {
            "description": "Тип парсера не найден",
            "content": {
                "application/json": {
                    "example": NotFoundError(ExceptionEnum.type_parser_not_found).exc_object
                }
            }
        }
    }
)
async def detail_order(
        order_id: str = Path(...,
                             title="Параметр order_id",
                             description="Параметр order_id для детальной информации о заказе",
                             min_length=24,
                             max_length=24),
):
    order = OrderService().get_by_id(order_id)
    order_model = Order.parse_obj(order.get("data"))
    if order_model.parser.type == TypeParser.maps.value:
        detail_order_model = MapOrderService.create_detail_order(order_model, order_dict=order)
        return WrapModel(
            data=detail_order_model
        )
    raise NotFoundError(ExceptionEnum.type_parser_not_found)


@parser_router.delete(
    "/orders/{order_id}",
    summary="Удалить заказ",
    description="Удалить заказ по id",
    response_description="Заказ успешно удален",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        422: {
            "description": "Order Id отсутствует",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "location": "path",
                            "field": "order_id",
                            "message": "field required",
                            "type": "type",
                        },
                        "body": {}
                    }
                }
            }
        },
        404: {
            "description": "Заказ с таким id не найден",
            "content": {
                "application/json": {
                    "example": NotFoundError(ExceptionEnum.order_not_found).exc_object
                }
            }
        }
    }
)
async def delete_order(
        order_id: str = Path(...,
                             title="Параметр order_id",
                             description="Параметр order_id для удаления заказа",
                             min_length=24,
                             max_length=24),
):
    deleted_status = OrderService().delete_by_id(order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
