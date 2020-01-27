from django.core import exceptions as django_extencions

from rest_framework import exceptions as rest_extencions

from apps.core.custom_exceptions import custom_exception_handler

EXC_MESSAGE = "error_message"


def check_response_data(response, status_code, error_code, exc_message):
    assert response.status_code == status_code
    assert response.data["error_code"] == error_code
    assert response.data["status_code"] == status_code
    response_messages = response.data["messages"]
    if type(response_messages) == list:
        for response_message in response_messages:
            assert response_message == exc_message
    else:
        assert response_messages == exc_message


def get_exception_and_context(rf, exc_class):
    context = {"request": rf.get("dummy")}
    exc = exc_class(EXC_MESSAGE)
    return context, exc


def test_custom_exception_handler_validation_error(rf):
    context, exc = get_exception_and_context(rf, django_extencions.ValidationError)
    status_code = 500
    error_code = "ValidationError"

    response = custom_exception_handler(exc, context)
    check_response_data(response, status_code, error_code, EXC_MESSAGE)


def test_exception_handler_not_found(rf):
    context, exc = get_exception_and_context(rf, rest_extencions.NotFound)
    status_code = exc.status_code
    error_code = exc.default_code

    response = custom_exception_handler(exc, context)
    check_response_data(response, status_code, error_code, EXC_MESSAGE)


def test_exception_handler_api_exception(rf):
    context, exc = get_exception_and_context(rf, rest_extencions.APIException)
    status_code = exc.status_code
    error_code = exc.default_code

    response = custom_exception_handler(exc, context)
    check_response_data(response, status_code, error_code, EXC_MESSAGE)


def test_exception_handler_permission_denied(rf):
    context, exc = get_exception_and_context(rf, rest_extencions.PermissionDenied)
    status_code = exc.status_code
    error_code = exc.default_code

    response = custom_exception_handler(exc, context)
    check_response_data(response, status_code, error_code, EXC_MESSAGE)


def test_exception_handler_method_not_allowed(rf):
    context, exc = get_exception_and_context(rf, rest_extencions.MethodNotAllowed)
    status_code = exc.status_code
    error_code = exc.default_code

    response = custom_exception_handler(exc, context)
    check_response_data(
        response, status_code, error_code, f'Method "{EXC_MESSAGE}" not allowed.'
    )


def test_exception_handler_auth_failed(rf):
    context, exc = get_exception_and_context(rf, rest_extencions.AuthenticationFailed)
    status_code = exc.status_code
    error_code = exc.default_code

    response = custom_exception_handler(exc, context)
    check_response_data(response, status_code, error_code, EXC_MESSAGE)


def test_exception_handler_non_auth(rf):
    context, exc = get_exception_and_context(rf, rest_extencions.NotAuthenticated)
    status_code = exc.status_code
    error_code = exc.default_code

    response = custom_exception_handler(exc, context)
    check_response_data(response, status_code, error_code, EXC_MESSAGE)


def test_exception_handler_parse_error(rf):
    context, exc = get_exception_and_context(rf, rest_extencions.ParseError)
    status_code = exc.status_code
    error_code = exc.default_code

    response = custom_exception_handler(exc, context)
    check_response_data(response, status_code, error_code, EXC_MESSAGE)
