from ast import alias
from unicodedata import name
from pydantic import BaseModel, Field
from bson.objectid import ObjectId


class AuthDetails(BaseModel):
    name: str
    username: str
    password: str


class PostSchema(BaseModel):
    id: int = Field(default=None, alias="_id")
    title: str = Field(default=None)
    content: str = Field(default=None)
    author: str = Field(default=None)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
