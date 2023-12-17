from rest_framework import serializers, exceptions


def custom_error(text_error: str, status_code_error: int=400) -> exceptions.ValidationError:
    """
    add serializers validation error status code
    """
    error = serializers.ValidationError(text_error)
    error.status_code = status_code_error
    return error

