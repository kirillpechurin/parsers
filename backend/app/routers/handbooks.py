from fastapi import APIRouter

from app.models.responses.wrap import WrapModel
from src.biz.services.handbooks_services.cities import CityService

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
