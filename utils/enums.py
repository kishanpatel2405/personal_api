from enum import Enum


class ErrorMessageCodes(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    BAD_REQUEST = "BAD_REQUEST"


class Currency(str, Enum):
    INR = "₹"


class Ip_Type(Enum):
    LOCAL = "local"
    EXTERNAL = "external"