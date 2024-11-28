from enum import Enum


class ErrorMessageCodes(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    BAD_REQUEST = "BAD_REQUEST"


class Gender(int, Enum):
    Male = "male"
    Female = "female"


class Currency(str, Enum):
    INR = "₹"
