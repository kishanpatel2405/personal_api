from .enums import ErrorMessageCodes


class ApiException(Exception):
    def __init__(self, msg: str, error_code: ErrorMessageCodes, status_code: int):
        self.msg = msg
        self.error_code = error_code
        self.status_code = status_code


class TokenError(Exception):
    pass


class TokenBackendError(Exception):
    pass
