from rest_framework import exceptions as rest_extencions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc: object, context: dict):
    response = exception_handler(exc, context)

    if response is None:
        response = Response(
            data=exc.messages,
            content_type="application/json",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if hasattr(response, "data"):
        if isinstance(exc, rest_extencions.APIException):
            exception_data = response.data["detail"]
            response.data = {"messages": exception_data.__str__()}
            response.data["error_code"] = exception_data.code
        elif isinstance(exc, Exception):
            response.data = {"messages": response.data}
            response.data["error_code"] = exc.__class__.__name__
        response.data["status_code"] = response.status_code

    headers = {}
    if isinstance(exc, rest_extencions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

    return Response(response.data, status=response.status_code, headers=headers)
