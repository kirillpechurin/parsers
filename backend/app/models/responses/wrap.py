from typing import Union

from pydantic import BaseModel, Field


class WrapModel(BaseModel):
    """
    Модель обертка для пользовательского вывода

    Является response_model для всех обработчиков
    """
    data: Union[dict, list, BaseModel] = Field(
        ...,
        title="Все экземпляры BaseModel и другие ответы",
        description="Поле служит как обертка для других результатов для достижения нужного ответа",
        example={"data": {"status": True}}
    )

    class Config:
        schema_extra = {
            "example": {
                "data": {"status": True}
            }
        }
