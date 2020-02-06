from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from apps.users.constants.messages import INVALID_TOKEN_MESSAGE

from .models import User


class CustomAccessToken(AccessToken):
    def __init__(self, token=None, verify=True):
        super().__init__(token, verify)
        user = User.objects.get(id=self.payload["user_id"])
        if str(user.security_hash) != self.payload["security_hash"]:
            raise TokenError(INVALID_TOKEN_MESSAGE)
