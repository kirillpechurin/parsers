from fastapi import APIRouter
from fastapi import status

from app.models.responses.wrap import WrapModel
from src.biz.services.handbooks_services.city import CityService
from src.biz.services.handbooks_services.example import ExampleService
from src.biz.exceptions.custom import NotFoundError


handbooks_router = APIRouter(
    prefix="/handbooks",
    tags=['handbooks']
)


@handbooks_router.get(
    "/cities",
    response_model=WrapModel,
    status_code=status.HTTP_200_OK,
    summary="Вывод всех городов",
    description="Метод на вывод всех доступных городов",
    response_description="Города успешно получены",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            "Пермь",
                            "Москва"
                        ]
                    }
                }
            }
        },
        404: {
            "content": {
                "application/json": {
                    "example": NotFoundError("Cities not found").exc_object
                }
            }
        }
    }
)
async def list_cities():
    cities = CityService().get_cities()
    return WrapModel(
        data=cities
    )


@handbooks_router.get(
    "/examples/maps",
    response_model=WrapModel,
    status_code=status.HTTP_200_OK,
    summary="Вывод всех городов",
    description="Метод на вывод всех доступных городов",
    response_description="Города успешно получены",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "type": "maps",
                            "examples": {
                                "json": {
                                    "data": {
                                        "address1": [
                                            {
                                                "name": "name",
                                                "text_review": "text_review"
                                            }
                                        ],
                                        "address2": [
                                            {
                                                "name": "name",
                                                "text_review": "text_review"
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        404: {
            "content": {
                "application/json": {
                    "example": NotFoundError("Cities not found").exc_object
                }
            }
        }
    }
)
async def examples():
    map_examples = ExampleService().get_maps_examples()
    return WrapModel(
        data={
            "type": "maps",
            "examples": map_examples
        }
    )
