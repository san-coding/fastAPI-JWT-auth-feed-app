# checks if request is authorized or not, verifies for protected routes

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import OAuth2PasswordRequestForm
from .jwt_handler import decodeJWT


class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            jwtBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=400,
                    detail="Invalid or expired token, please login again",
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=400, detail="Invalid or expired token, please login again"
            )

    def verify_jwt(self, jwttoken: str):
        isTokenValid: bool = False  # false flag

        payload = decodeJWT(jwttoken)
        if payload:
            isTokenValid = True
        return isTokenValid
