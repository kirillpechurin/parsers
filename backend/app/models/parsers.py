from pydantic import BaseModel, HttpUrl


class Map(BaseModel):
    name: str
    correct: bool
    link: HttpUrl
    image_link: str
