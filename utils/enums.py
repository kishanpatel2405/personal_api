from enum import Enum


class ErrorMessageCodes(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    BAD_REQUEST = "BAD_REQUEST"
