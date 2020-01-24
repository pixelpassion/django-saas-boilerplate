from unittest.mock import patch

from django.core import exceptions as django_extencions
from django.urls import reverse

from rest_framework import exceptions as rest_extencions

EXC_MESSAGES = "error_message"


def test_exception_handler_validation_error(client, mocker):
    status_code = 400
    error_code = "error_code"
    with patch(
        "apps.core.views.TestApiView.post",
        side_effect=django_extencions.ValidationError(EXC_MESSAGES),
    ):
        response = client.post(reverse("v0:handler-test-url"))
        assert response.status_code == status_code
        assert response.data["messages"] == [EXC_MESSAGES]
        assert response.data["error_code"] == error_code
        assert response.data["status_code"] == status_code


def test_exception_handler_not_found(client, mocker):
    status_code = 404
    error_code = "not_found"
    with patch(
        "apps.core.views.TestApiView.post",
        side_effect=rest_extencions.NotFound(EXC_MESSAGES),
    ):
        response = client.post(reverse("v0:handler-test-url"))
        assert response.status_code == status_code
        assert response.data["messages"] == EXC_MESSAGES
        assert response.data["error_code"] == error_code
        assert response.data["status_code"] == status_code


def test_exception_handler_api_exception(client, mocker):
    status_code = 500
    error_code = "error"
    with patch(
        "apps.core.views.TestApiView.post",
        side_effect=rest_extencions.APIException(EXC_MESSAGES),
    ):
        response = client.post(reverse("v0:handler-test-url"))
        assert response.status_code == status_code
        assert response.data["messages"] == EXC_MESSAGES
        assert response.data["error_code"] == error_code
        assert response.data["status_code"] == status_code


def test_exception_handler_permission_denied(client, mocker):
    status_code = 403
    error_code = "permission_denied"
    with patch(
        "apps.core.views.TestApiView.post",
        side_effect=rest_extencions.PermissionDenied(EXC_MESSAGES),
    ):
        response = client.post(reverse("v0:handler-test-url"))
        assert response.status_code == status_code
        assert response.data["messages"] == EXC_MESSAGES
        assert response.data["error_code"] == error_code
        assert response.data["status_code"] == status_code


def test_exception_handler_method_not_allowed(client, mocker):
    status_code = 405
    error_code = "method_not_allowed"
    with patch(
        "apps.core.views.TestApiView.post",
        side_effect=rest_extencions.MethodNotAllowed(EXC_MESSAGES),
    ):
        response = client.post(reverse("v0:handler-test-url"))
        assert response.status_code == status_code
        assert response.data["messages"] == f'Method "{EXC_MESSAGES}" not allowed.'
        assert response.data["error_code"] == error_code
        assert response.data["status_code"] == status_code


def test_exception_handler_auth_failed(client, mocker):
    status_code = 401
    error_code = "authentication_failed"
    with patch(
        "apps.core.views.TestApiView.post",
        side_effect=rest_extencions.AuthenticationFailed(EXC_MESSAGES),
    ):
        response = client.post(reverse("v0:handler-test-url"))
        assert response.status_code == status_code
        assert response.data["messages"] == EXC_MESSAGES
        assert response.data["error_code"] == error_code
        assert response.data["status_code"] == status_code


def test_exception_handler_non_auth(client, mocker):
    status_code = 401
    error_code = "not_authenticated"
    with patch(
        "apps.core.views.TestApiView.post",
        side_effect=rest_extencions.NotAuthenticated(EXC_MESSAGES),
    ):
        response = client.post(reverse("v0:handler-test-url"))
        assert response.status_code == status_code
        assert response.data["messages"] == EXC_MESSAGES
        assert response.data["error_code"] == error_code
        assert response.data["status_code"] == status_code
