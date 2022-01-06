from fastapi import APIRouter

from app.models.responses.wrap import WrapModel
from src.biz.services.handbooks_services.city import CityService
from src.biz.services.handbooks_services.example import ExampleService


handbooks_router = APIRouter(
    prefix="/handbooks",
    tags=['handbooks']
)


@handbooks_router.get("/cities")
async def list_cities():
    cities = CityService().get_cities()
    return WrapModel(
        data=cities
    )


@handbooks_router.get("/examples/maps")
async def examples():
    map_examples = ExampleService().get_maps_examples()
    return WrapModel(
        data={
            "type": "maps",
            "examples": map_examples
        }
    )
