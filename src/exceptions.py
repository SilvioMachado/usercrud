from typing import Type
from werkzeug.exceptions import HTTPException


class InvalidException(HTTPException):
    code = 400


class InvalidRequestSchemaError(HTTPException):
    code = 400


def handle_bad_request(e: Type[Exception]):
    return str(e), 400
