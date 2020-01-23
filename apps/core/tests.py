from unittest.mock import patch

from django.core import exceptions
from django.urls import reverse


def test_exception_handler_validation_error(client, mocker):
    exc_messages = ["first message", "second message"]
    status_code = 400
    error_code = "error_code"
    with patch(
        "apps.core.views.TestApiView.post",
        side_effect=exceptions.ValidationError(exc_messages),
    ):
        response = client.post(reverse("v0:handler-test-url"))
        assert response.status_code == status_code
        response.data["messages"] == exc_messages
        response.data["error_code"] == error_code
        response.data["status_code"] == status_code
