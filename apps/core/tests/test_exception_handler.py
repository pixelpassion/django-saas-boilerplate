from django.core import exceptions as django_extencions

import pytest
from rest_framework import exceptions as rest_extencions

from apps.core.custom_exceptions import custom_exception_handler

EXC_MESSAGE = "error_message"


def check_response_data(response, status_code, error_code, exc_message):
    assert response.status_code == status_code
    assert response.data["error_code"] == [error_code]
    assert response.data["status_code"] == status_code
    response_messages = response.data["messages"]
    assert exc_message in response_messages


def get_exception_and_context(rf, exc_class):
    context = {"request": rf.get("dummy")}
    exc = exc_class(EXC_MESSAGE)
    return context, exc


@pytest.mark.parametrize(
    "exc",
    [
        django_extencions.FieldDoesNotExist,
        django_extencions.ObjectDoesNotExist,
        django_extencions.SuspiciousOperation,
        django_extencions.DisallowedHost,
        django_extencions.RequestDataTooBig,
        django_extencions.ViewDoesNotExist,
        django_extencions.FieldError,
        django_extencions.ValidationError,
    ],
)
def test_custom_exception_handler_django_extencions(rf, exc):
    context, exc = get_exception_and_context(rf, exc)
    status_code = 500
    error_code = exc.__class__.__name__

    response = custom_exception_handler(exc, context)
    check_response_data(response, status_code, error_code, EXC_MESSAGE)


@pytest.mark.parametrize(
    "exc",
    [
        rest_extencions.NotFound,
        rest_extencions.APIException,
        rest_extencions.PermissionDenied,
        rest_extencions.AuthenticationFailed,
        rest_extencions.MethodNotAllowed,
        rest_extencions.NotAuthenticated,
        rest_extencions.ParseError,
    ],
)
def test_custom_exception_handler_rest_extencions(rf, exc):
    context, exc = get_exception_and_context(rf, exc)
    status_code = exc.status_code
    error_code = exc.default_code

    message = EXC_MESSAGE
    if exc.__class__ == rest_extencions.MethodNotAllowed:
        message = f'Method "{EXC_MESSAGE}" not allowed.'

    response = custom_exception_handler(exc, context)
    check_response_data(response, status_code, error_code, message)
