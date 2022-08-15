from werkzeug.exceptions import HTTPException


class InvalidException(HTTPException):
    code = 400


def handle_invalid_exception(e: InvalidException):
    return str(e), 400
