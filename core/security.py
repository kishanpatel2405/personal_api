import base64
import hashlib
from typing import List

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from utils.enums import RoleEnum


def verify_hash(password, saved_salt):
    saved_salt = saved_salt.encode("utf-8")
    saved_salt = base64.b64decode(saved_salt)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        saved_salt,
        100000,
    )
    key = base64.b64encode(key)
    return key
