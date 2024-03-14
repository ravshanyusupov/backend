import ninja_jwt
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import IntegrityError
from ninja.errors import HttpError
from ninja_lib.error.exceptions import DomainException
from ninja_lib.error.pydantic_translations import ERROR_NAMES_RU, ERROR_NAMES_UZ
from ninja_lib.error.db_check import get_integrity_error_code
from ninja_lib.logger import logger

from ninja.errors import ValidationError
from pydantic_core import ValidationError as PyValidationError
from src.apps.core.errors import generate_error_response
from src.apps.core.errors.status import STATUS_CODES

from typing import Union

ERROR_CODES_MAP = {
    "uz": ERROR_NAMES_UZ,
    "ru": ERROR_NAMES_RU,
}

ERRORS_LANGUAGE_CODES = ["uz", "ru"]


def get_error_message(
    lang_code: list = ERRORS_LANGUAGE_CODES, error_type: str = "", ctx: dict = None
):
    result = dict()

    for code in lang_code:
        message = ERROR_CODES_MAP[code].get(error_type, "")
        result[f"name_{code}"] = message.format(**ctx) if ctx else message

    return result


def convert_errors(e: Union[ValidationError, PyValidationError]):
    new_errors = []
    errors = e.errors

    if isinstance(e, PyValidationError):
        errors = e.errors()

    for error in errors:
        exc_type = error.get("type", "")
        exc_ctx = error.get("ctx", None)
        custom_message_dict = get_error_message(error_type=exc_type, ctx=exc_ctx)
        error_structure = {"code": error["type"], "location": error["loc"]}
        error_structure.update(custom_message_dict)
        new_errors.append(error_structure)
    return new_errors


def inspect_global_exceptions(exc):
    global_exceptions = [
        # Exception, error_code
        (ninja_jwt.exceptions.TokenError, 1001),
        (ObjectDoesNotExist, 1002),
        (PermissionDenied, 1000),
        (IntegrityError, get_integrity_error_code),
    ]

    for exception, error_code in global_exceptions:
        if isinstance(exc, exception):
            if callable(error_code):
                return error_code(exc)
            return error_code

    return 0


def catch_errors(api_instance):
    @api_instance.exception_handler(ValidationError)
    @api_instance.exception_handler(PyValidationError)
    def pydantic_validation_error_handler(request, exc):
        errors = convert_errors(exc)
        return api_instance.create_response(request, errors, status=400)

    @api_instance.exception_handler(Exception)
    def global_error_handler(request, exc: Exception):
        DEFAULT_STATUS = 500

        # if status == 500:
        #     logger.error(exc, exc_info=True)

        error_code = 0

        if isinstance(exc, DomainException):
            error_code = exc.code
            error_ctx = exc.ctx

            error_response = [
                generate_error_response(
                    error_code=code, lang=ERRORS_LANGUAGE_CODES, ctx=error_ctx
                ) for code in error_code
            ]

            if len(error_code) == 1:
                status = STATUS_CODES.get(error_code[0], DEFAULT_STATUS)
            else:
                status = 400

        else:
            error_code = inspect_global_exceptions(exc)
            error_ctx = None
            error_response = [
                generate_error_response(
                    error_code=error_code, lang=ERRORS_LANGUAGE_CODES, ctx=error_ctx
                )
            ]

            status = STATUS_CODES.get(error_code, DEFAULT_STATUS)

        return api_instance.create_response(request, error_response, status=status)
