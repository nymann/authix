from http import HTTPStatus

from fastapi import HTTPException


class Unauthorized(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorized")


class Conflict(HTTPException):
    def __init__(self, detail: str = "Conflict") -> None:
        super().__init__(status_code=HTTPStatus.CONFLICT, detail=detail)
