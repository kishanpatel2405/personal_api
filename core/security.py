import base64
import hashlib
from typing import List

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from schemas.v1.token import AccessToken, RefreshToken
from utils.enums import RoleEnum
from utils.errors import TokenError


def verify_hash(password, saved_salt):
    # Salt is in utf-8 string I need to encode it in Base64 and then decode the Base64 to bytes
    saved_salt = saved_salt.encode("utf-8")
    saved_salt = base64.b64decode(saved_salt)
    key = hashlib.pbkdf2_hmac(
        "sha256",  # The hash digest algorithm for HMAC
        password.encode("utf-8"),  # Convert the password to bytes
        saved_salt,  # Provide the salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
    )
    key = base64.b64encode(key)
    return key


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            try:
                return self.verify_jwt(credentials.credentials)
            except TokenError as e:
                raise HTTPException(status_code=403, detail=str(e))
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str):
        ...


class JWTAccessTokenBearer(JWTBearer):
    def verify_jwt(self, jwt_token: str):
        return AccessToken(jwt_token)


class JWTRefreshTokenBearer(JWTBearer):
    def verify_jwt(self, jwt_token: str):
        return RefreshToken(jwt_token)


class RoleChecker:
    def __init__(self, required_roles: List[RoleEnum]) -> None:
        self.required_roles = required_roles

    async def __call__(self, token: dict = Depends(JWTAccessTokenBearer())) -> dict:
        if RoleEnum[token["role"]] not in self.required_roles:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permissions")
        return token
