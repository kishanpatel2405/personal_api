import base64
import hashlib
import os
import re
from datetime import datetime
from urllib.parse import urljoin
from uuid import uuid4

from sqlalchemy import exists
from sqlalchemy.orm import Session, joinedload

from config import config
from models import Role, UnderMaintenance, User, UserEmailToken
from utils.enums import RoleEnum, TokenType


def get_name_from_email(email: str):
    match = re.match(r"^[a-zA-Z]+", email.split("@")[0])
    name = match.group()
    result = name
    return result


def get_role(db: Session, role: RoleEnum):
    return db.query(Role).filter(Role.name == role.name).first()


def verify_email_token(db: Session, token: str):
    # Retrieve the token from the database.
    db_token = db.query(UserEmailToken).filter(UserEmailToken.user_token == token).first()

    # Ensure token exists in the database.
    if not db_token:
        return False

    # Calculate the time difference in hours.
    difference = datetime.utcnow() - db_token.time
    hours = difference.total_seconds() / 3600

    if hours > config.USER_EMAIL_VERIFICATION_TOKEN_EXPIRATION_TIME_IN_HOURS:
        # If the token is expired, return False.
        return False

    # If token is not expired, verify the associated user and commit changes.
    db_user = db.query(User).filter(User.id == db_token.user_id).first()
    db_user.is_verified = True
    db_token.is_used = True
    db.commit()

    return True


def create_link_for_user_email_verification(token: str):
    base_url = config.FRONTEND_URL
    url_with_token = f"/email-verification/?token={token}"

    return urljoin(base_url, url_with_token)


def get_email_from_id(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    return db_user.email


def create_token(db: Session, user_id: int, token_type: TokenType):
    token = uuid4().hex
    db_token = UserEmailToken(user_id=user_id, user_token=token, type=token_type)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return token


def check_user_exists(db: Session, email: str):
    ((ret,),) = db.query(exists().where(User.email == email))
    return ret


def set_password(db: Session, password: str, user_id: int):
    db_user = get_user_by_id(db, user_id)
    encoded_salt, encoded_key = generate_encoded_password(password)

    db_user.hashed_password = encoded_key.decode("utf-8")
    db_user.salt = encoded_salt.decode("utf-8")
    db.commit()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_profile_details(db: Session, user_id: int):
    return (
        db.query(User)
        .options(joinedload(User.country), joinedload(User.state), joinedload(User.city))
        .filter(User.id == user_id)
        .first()
    )


def generate_encoded_password(password: str):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        "sha256",  # The hash digest algorithm for HMAC
        password.encode("utf-8"),  # Convert the password to bytes
        salt,  # Provide the salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
    )
    # Bytes encoded to Base64 but still in byte format
    encoded_salt = base64.b64encode(salt)
    encoded_key = base64.b64encode(key)

    return encoded_salt, encoded_key


def reset_user_password(db: Session, token: str, user_id: int, password: str):
    db_token = db.query(UserEmailToken).filter(UserEmailToken.user_token == token).first()
    user = get_user_by_id(db, user_id)
    set_password(db, password, user.id)
    db_token.is_used = True
    db.commit()
    db.refresh(db_token)


def create_link_for_forgot_password_email_verification(token: str):
    base_url = config.FRONTEND_URL
    url_with_token = f"/forgot-password/?token={token}"

    return urljoin(base_url, url_with_token)


def verify_forgot_password_token(db: Session, token: str):
    db_token = db.query(UserEmailToken).filter(UserEmailToken.user_token == token).first()

    if not db_token:
        return "invalid token"

    if db_token.type == TokenType.EmailVerificationToken:
        return "invalid token"

    if db_token.is_used is True:
        return "already verified"

    difference = datetime.utcnow() - db_token.time
    hours = difference.total_seconds() / 3600

    if hours > config.USER_FORGOT_PASSWORD_TOKEN_EXPIRATION_TIME_IN_HOURS:
        return "time expired"

    return True


def get_user_by_verification_token(db: Session, token: str):
    db_token = db.query(UserEmailToken).filter(UserEmailToken.user_token == token).first()
    if db_token:
        return db_token
    return False


async def get_maintenance_status(db: Session):
    maintenance_status = db.query(UnderMaintenance).first()
    return maintenance_status
