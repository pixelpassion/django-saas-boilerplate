from unittest.mock import patch

from django.core import exceptions as django_extencions
from django.urls import reverse

from rest_framework import exceptions as rest_extencions

EXC_MESSAGE = "error_message"


def _check_response_data(response, status_code, error_code, exc_message):
    assert response.status_code == status_code
    assert response.data["error_code"] == error_code
    assert response.data["status_code"] == status_code
    response_messages = response.data["messages"]
    if type(response_messages) == list:
        for response_message in response_messages:
            assert response_message == exc_message
    else:
        assert response_messages == exc_message


def _mock_view_make_request(client, exc_class):
    with patch("apps.core.views.TestApiView.post", side_effect=exc_class(EXC_MESSAGE)):
        return client.post(reverse("v0:handler-test-url"))


def test_exception_handler_validation_error(client, mocker):
    status_code = 500
    error_code = "ValidationError"
    response = _mock_view_make_request(client, django_extencions.ValidationError)
    _check_response_data(response, status_code, error_code, EXC_MESSAGE)


def test_exception_handler_not_found(client, mocker):
    status_code = 404
    error_code = "not_found"
    response = _mock_view_make_request(client, rest_extencions.NotFound)
    _check_response_data(response, status_code, error_code, EXC_MESSAGE)


def test_exception_handler_api_exception(client, mocker):
    status_code = 500
    error_code = "error"
    response = _mock_view_make_request(client, rest_extencions.APIException)
    _check_response_data(response, status_code, error_code, EXC_MESSAGE)


def test_exception_handler_permission_denied(client, mocker):
    status_code = 403
    error_code = "permission_denied"
    response = _mock_view_make_request(client, rest_extencions.PermissionDenied)
    _check_response_data(response, status_code, error_code, EXC_MESSAGE)


def test_exception_handler_method_not_allowed(client, mocker):
    status_code = 405
    error_code = "method_not_allowed"
    response = _mock_view_make_request(client, rest_extencions.MethodNotAllowed)
    _check_response_data(
        response, status_code, error_code, f'Method "{EXC_MESSAGE}" not allowed.'
    )


def test_exception_handler_auth_failed(client, mocker):
    status_code = 403
    error_code = "authentication_failed"
    response = _mock_view_make_request(client, rest_extencions.AuthenticationFailed)
    _check_response_data(response, status_code, error_code, EXC_MESSAGE)


def test_exception_handler_non_auth(client, mocker):
    status_code = 403
    error_code = "not_authenticated"
    response = _mock_view_make_request(client, rest_extencions.NotAuthenticated)
    _check_response_data(response, status_code, error_code, EXC_MESSAGE)


def test_exception_handler_parse_error(client, mocker):
    status_code = 400
    error_code = "parse_error"
    response = _mock_view_make_request(client, rest_extencions.ParseError)
    _check_response_data(response, status_code, error_code, EXC_MESSAGE)
