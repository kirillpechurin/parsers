from enum import Enum
from typing import Union

from pydantic import BaseModel, HttpUrl, Field


class Map(BaseModel):
    name: str
    correct: bool
    link: HttpUrl
    image_link: str


class TypeParser(str, Enum):
    maps = "maps"


class MapData(BaseModel):
    city: str = Field(
        ...,
        title="Город, в котором нужно спарсить информацию",
        description="Параметр city, является одним из двух ключевых параметров для парсинга",
        example="Пермь"
    )
    organisation: str = Field(
        ...,
        title="Организация, по филиалам/объекту которой нужно спарсить информацию",
        description="Параметр organisation, является вторым важным паметром для парсинга данных с карт",
        example="Monkey Grinder"
    )

    class Config:
        schema_extra = {
            "example": {
                "city": "Пермь",
                "organisation": "Monkey Grinder",
            }
        }


class OrderParser(BaseModel):
    name: str = Field(
        ...,
        title="Name of parser instance",
        description="Поле name для выбора парсера, зависит от типа",
        example="2gis"
    )
    type: str = Field(
        ...,
        title="Type of parser",
        description="Тип парсера, пока только карты",
        example="maps"
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "2gis",
                "type": "maps"
            }
        }


class Order(BaseModel):
    data: Union[MapData] = Field(
        ...,
        title='Объект данных для парсинга',
        description="В данные входит нужная информация для самого парсинга (город - организация)",
        example={"city": 'Пермь', "organisation": "Monkey Grinder"}
    )
    parser: OrderParser = Field(
        ...,
        title="Объект данных парсера",
        description="Служит для выбора парсера по типу и предопределенному имени",
        example={"type": "maps", "name": "2gis"}
    )

    class Config:
        schema_extra = {
            "example": {
                "data": MapData.Config.schema_extra.get("example"),
                "parser": OrderParser.Config.schema_extra.get("example")
            }
        }
