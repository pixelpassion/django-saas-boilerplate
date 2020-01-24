from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    handlers = {
        "ValidationError": _handle_validation_error,
        "NotFound": _handle_not_found_error,
        "APIException": _handle_api_exception_error,
        "PermissionDenied": _handle_permission_denied_error,
        "MethodNotAllowed": _handle_method_not_allowed_error,
        "AuthenticationFailed": _handle_non_auth_error,
        "NotAuthenticated": _handle_non_auth_error,
    }

    # Lets dentify the type of the current exception to check if we should handle it
    exception_class = exc.__class__.__name__

    # Some errors do not give an Response. We need to handle this case as well
    if response is None:
        response = Response(
            data=exc.messages,
            content_type="application/json",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # If this exception is one that we can handle, handle it.
    if exception_class in handlers:
        try:
            return handlers[exception_class](exc, context, response)
        except Exception:
            pass

    return _handle_generic_error(exc, context, response)


def _handle_generic_error(exc, context, response):
    response.data["status_code"] = response.status_code

    headers = {}

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

    return Response(response.data, status=response.status_code, headers=headers)


def _handle_validation_error(exc, context, response):
    response.status_code = status.HTTP_400_BAD_REQUEST
    if hasattr(response, "data"):
        response.data = {"messages": response.data}
    response.data["error_code"] = "error_code"
    return _handle_generic_error(exc, context, response)


def _handle_not_found_error(exc, context, response):
    response.status_code = status.HTTP_404_NOT_FOUND
    if hasattr(response, "data"):
        exception_data = response.data["detail"]
        response.data = {"messages": exception_data.__str__()}
    response.data["error_code"] = exception_data.code
    return _handle_generic_error(exc, context, response)


def _handle_api_exception_error(exc, context, response):
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    if hasattr(response, "data"):
        exception_data = response.data["detail"]
        response.data = {"messages": exception_data.__str__()}
    response.data["error_code"] = exception_data.code
    return _handle_generic_error(exc, context, response)


def _handle_permission_denied_error(exc, context, response):
    response.status_code = status.HTTP_403_FORBIDDEN
    if hasattr(response, "data"):
        exception_data = response.data["detail"]
        response.data = {"messages": exception_data.__str__()}
    response.data["error_code"] = exception_data.code
    return _handle_generic_error(exc, context, response)


def _handle_method_not_allowed_error(exc, context, response):
    response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    if hasattr(response, "data"):
        exception_data = response.data["detail"]
        response.data = {"messages": exception_data.__str__()}
    response.data["error_code"] = exception_data.code
    return _handle_generic_error(exc, context, response)


def _handle_non_auth_error(exc, context, response):
    response.status_code = status.HTTP_401_UNAUTHORIZED
    if hasattr(response, "data"):
        exception_data = response.data["detail"]
        response.data = {"messages": exception_data.__str__()}
    response.data["error_code"] = exception_data.code
    return _handle_generic_error(exc, context, response)
