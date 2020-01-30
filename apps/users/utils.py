from .serializers import UserRegistrationSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    return UserRegistrationSerializer(user, context={"request": request}).data
