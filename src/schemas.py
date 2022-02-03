from unicodedata import name
from pydantic import BaseModel


class AuthDetails(BaseModel):
    name: str
    username: str
    password: str
