from pydantic import BaseModel, conint


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    is_enterprise: bool = False


class UserLogin(UserBase):
    password: str


class ChangePassword(BaseModel):
    password: str
    new_password: str


class UserUpdate(BaseModel):
    title: str
    first_name: str
    last_name: str
    gender: str
    mobile_number: conint(gt=999999999, lt=10000000000)
    address: str
    city: str
    date_of_birth: date
