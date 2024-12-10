from enum import Enum


class ErrorMessageCodes(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    BAD_REQUEST = "BAD_REQUEST"


class Currency(str, Enum):
    INR = "₹"


class Ip_Type(Enum):
    LOCAL = "local"
    EXTERNAL = "external"


class RoleEnum(str, Enum):
    User = 1
    Admin = 2
    SuperAdmin = 3


class TokenType(int, Enum):
    EmailVerificationToken = 1
    ForgotPasswordToken = 2


class Environment(str, Enum):
    TEST = "test"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

    def __str__(self):
        return self.value
