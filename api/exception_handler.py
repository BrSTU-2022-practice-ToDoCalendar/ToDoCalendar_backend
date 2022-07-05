from rest_framework.views import exception_handler
from rest_framework.validators import ValidationError


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        field, error = list(response.data.items())[0]
        if isinstance(error, list):
            error_message = error[0]
        elif isinstance(error, dict):
            error_message = list(error.items())[0][1]
        else:
            error_message = error

        response.data = {field: error_message}

    return response
