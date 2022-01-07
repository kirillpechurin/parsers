from typing import Union

from pydantic import BaseModel


class WrapModel(BaseModel):
    data: Union[dict, list, BaseModel]
