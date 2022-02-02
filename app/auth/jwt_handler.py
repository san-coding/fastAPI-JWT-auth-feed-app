# this file is used to create, verifying, signing, encoding, decoding and returning jwt tokens
import time
import jwt
from decouple import config

JWT_SECRET_KEY = config("JWT_SECRET_KEY")
JWT_ALGORITHM = config("JWT_ALGORITHM")
