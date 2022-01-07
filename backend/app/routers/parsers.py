from fastapi import APIRouter, Depends
from starlette import status

from app.dependences.auth import get_current_account
from src.biz.exceptions.custom import ValidationError

from app.models.responses.wrap import WrapModel
from src.biz.services.parsers_services.map_service import MapService

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
