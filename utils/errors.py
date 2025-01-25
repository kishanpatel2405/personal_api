from fastapi import HTTPException

from .enums import ErrorMessageCodes


class ApiException(HTTPException):
    def __init__(self, msg: str, error_code: ErrorMessageCodes, status_code: int):
        super().__init__(status_code=status_code, detail=msg)
        self.msg = msg
        self.error_code = error_code
        self.status_code = status_code


