from unicodedata import name
from pydantic import BaseModel, Field


class AuthDetails(BaseModel):
    name: str
    username: str
    password: str


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(default=None)
    content: str = Field(default=None)
    author: str = Field(default=None)
