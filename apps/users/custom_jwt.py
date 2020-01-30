from calendar import timegm
from datetime import datetime
from typing import Dict

import jwt
from rest_framework import exceptions
from rest_framework_jwt.compat import get_username
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_get_secret_key

from .models import User


def custom_jwt_payload_handler(user: User) -> Dict:
    """ Custom payload handler
        Token encrypts the dictionary returned by this function, and can be decoded
        by rest_framework_jwt.utils.jwt_decode_handler
    """
    return {
        "user_id": user.pk,
        "username": get_username(user),
        "exp": datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        "orig_iat": timegm(datetime.utcnow().utctimetuple()),
        "security_hash": str(user.security_hash),
    }


def custom_jwt_decode_handler(token: str) -> Dict:
    options = {"verify_exp": api_settings.JWT_VERIFY_EXPIRATION}
    # get user from token, BEFORE verification, to get user secret key
    unverified_payload = jwt.decode(token, None, False)
    instance = User.objects.filter(id=unverified_payload["user_id"]).first()
    if instance and str(instance.security_hash) != unverified_payload["security_hash"]:
        raise exceptions.AuthenticationFailed()
    secret_key = jwt_get_secret_key(unverified_payload)
    return jwt.decode(
        token,
        api_settings.JWT_PUBLIC_KEY or secret_key,
        api_settings.JWT_VERIFY,
        options=options,
        leeway=api_settings.JWT_LEEWAY,
        audience=api_settings.JWT_AUDIENCE,
        issuer=api_settings.JWT_ISSUER,
        algorithms=[api_settings.JWT_ALGORITHM],
    )
