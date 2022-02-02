# this file is used to create, verifying, signing, encoding, decoding and returning jwt tokens
import time
import jwt
from decouple import config

JWT_SECRET_KEY = config("JWT_SECRET_KEY")
JWT_ALGORITHM = config("JWT_ALGORITHM")

# return a jwt token
def token_response(token: str):
    return {"access token": token}


def signJWT(userID: str):
    # creating a payload
    payload = {"userID": userID, "expiry": time.time() + 1200}
    # signing the payload
    token = jwt.encode(payload, JWT_SECRET_KEY, JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    # decoding the payload
    try:
        decode_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token["expiry"] >= time.time() else None
    except:
        return {"error": "Invalid token"}
