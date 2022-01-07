import datetime
from enum import Enum
from typing import Union

import pytz
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


class MapReviews(BaseModel):
    html_filename: str = Field(
        ...,
        title='Имя html файла отзывов',
        description="Это html file с отрисовкой всех отзывов",
        exampple="reviews_gishfg83yq8r4437r4h7834873.html"
    )
    data: dict = Field(
        ...,
        title="Результаты парсинга",
        description="Содержит результаты парсинга",
        example={"address1": [{"name": "name", "text_review": "text_review"},],
                 "address2": [{"name": "name", "text_review": "text-review"},]}
    )

    class Config:
        schema_extra = {
            "example": {
                "filename": "reviews_gishfg83yq8r4437r4h7834873.html",
                "data": {"address1": [{"name": "name", "text_review": "text_review"}, ],
                         "address2": [{"name": "name", "text_review": "text-review"}, ]},
            }
        }


class DetailOrder(BaseModel):
    order_id: str = Field(
        ...,
        title="Id заказа",
        description="Id заказа",
        example="order_id"
    )
    data: Order = Field(
        ...,
        title="Объект данных заказа",
        description="Содержит данные по парсеру и данные для парсинга",
        example=Order.Config.schema_extra.get("example")
    )
    created_at: datetime.datetime = Field(
        ...,
        title="Дата создания заказа",
        description="Дата создания заказа",
        example=datetime.datetime.now(tz=pytz.UTC)
    )
    result: Union[MapReviews] = Field(
        None,
        title="Результаты",
        description="Содержит объект результатов парсинга",
        example=MapReviews.Config.schema_extra.get("example")
    )

    class Config:
        schema_extra = {
            "example": {
                "order_id": "order-id",
                "data": Order.Config.schema_extra.get("example"),
                "created_at": datetime.datetime.now(tz=pytz.UTC),
                "result": MapReviews.Config.schema_extra.get("example")
            }
        }
