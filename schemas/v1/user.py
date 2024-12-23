from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, conint

from schemas.v1.token import Token


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    is_enterprise: bool = False


class UserLogin(UserBase):
    password: str
    is_enterprise: bool = False


class UserLoginResponse(Token): ...


class ChangePassword(BaseModel):
    password: str
    new_password: str


class UserUpdate(BaseModel):
    title: str
    first_name: str
    last_name: str
    gender: str
    passport_no: str | None
    passport_expiry: datetime | None
    passport_issue_date: datetime | None
    cell_country_code: str
    mobile_number: conint(gt=999999999, lt=10000000000)
    address: str
    city: str
    date_of_birth: date


class CountryResponse(BaseModel):
    id: int
    name: str
    iso2: str
    iso3: str
    phone_code: str
    currency: str
    currency_name: str
    currency_symbol: str
    emoji: str
    emoji_iu: str


class StateResponse(BaseModel):
    id: int
    name: str
    status_code: str
    country_id: int


class CityResponse(BaseModel):
    id: int
    name: str
    state_id: int


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    title: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    passport_no: Optional[str] = None
    passport_expiry: Optional[date] = None
    passport_issue_date: Optional[date] = None
    cell_country_code: Optional[str] = None
    mobile_number: Optional[int] = None
    address: Optional[str] = None
    country: Optional[CountryResponse] = None
    state: Optional[StateResponse] = None
    city: Optional[CityResponse] = None
    date_of_birth: Optional[date] = None
    company_id: Optional[int] = None
    is_verified: bool
    profile_image_url: str
    maintenance: bool


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
