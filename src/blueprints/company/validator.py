from typing import Type
from flask import request
from marshmallow import Schema, fields, validate, ValidationError
from src.exceptions import InvalidRequestSchemaError


class CompanyBankAccount(Schema):
    """
    Representation of CompanyBankAccount model
    """
    agency = fields.String(validate=validate.Length(max=10))
    account_number = fields.String(validate=validate.Length(max=10))
    bank_code = fields.String(validate=validate.Length(min=1, max=3))


class CompanyRequest(Schema):
    """
    Validate request to create/update company
    """
    company_name = fields.String()
    phone = fields.Integer()
    declared_billing = fields.Decimal()
    bank_accounts = fields.List(fields.Nested(CompanyBankAccount()))


class BankRequest(CompanyBankAccount):
    """
    Validate request to create/update a bank account
    """
    pass


def validate_request_body(schema: Type[Schema] = None):
    """
    Decorator for Flask request body validation. Useful for request data in
    application/json format.

    Usage:
        @app.route('/my-route')
        @validate_request_body(schema=CreateCompanyRequest)
        def view():
            ...
    """
    def validate_decorator(func):
        def wrapper(*args, **kwargs):
            if schema:
                try:
                    schema().load(request.json)
                except ValidationError as e:
                    # HTTP safe error.
                    raise InvalidRequestSchemaError(str(e))

            return func(*args, **kwargs)

        # https://stackoverflow.com/questions/17256602/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi
        wrapper.__name__ = func.__name__
        return wrapper

    return validate_decorator
