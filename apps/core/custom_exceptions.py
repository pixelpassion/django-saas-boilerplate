from rest_framework import exceptions as rest_extencions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc: object, context: dict):
    response = exception_handler(exc, context)
    if response is None:
        response = Response(
            data=exc.args,
            content_type="application/json",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if hasattr(response, "data"):
        if isinstance(exc, rest_extencions.APIException):
            exception_details = response.data.get("detail")
            messages = []
            error_codes = []
            if exception_details:
                messages.append(exception_details.__str__())
                error_codes.append(exception_details.code)
            else:
                for key, value in response.data.items():
                    messages.append(f"{key}: {value[0].__str__()}")
                    error_codes.append(value[0].code)
            response.data = {"messages": messages}
            response.data["error_code"] = error_codes
        elif isinstance(exc, Exception):
            response.data = {"messages": response.data}
            response.data["error_code"] = [exc.__class__.__name__]
        response.data["status_code"] = response.status_code

    headers = {}
    if isinstance(exc, rest_extencions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

    return Response(response.data, status=response.status_code, headers=headers)
