import pytest
from rest_framework.exceptions import ValidationError

from apps.users.constants.messages import (
    NO_REQUEST_IN_CONTEXT_MESSAGE,
    NO_USER_IN_REQUEST_MESSAGE,
)
from apps.users.serializers import CustomPasswordChangeSerializer


def test_pass_change_setializer_without_request():
    with pytest.raises(ValidationError) as em:
        CustomPasswordChangeSerializer(context={})
    assert NO_REQUEST_IN_CONTEXT_MESSAGE == em.value.args[0]


def test_pass_change_setializer_without_user_in_request(rf):
    request = rf.get("DUMMY")
    assert not getattr(request, "user", None)
    with pytest.raises(ValidationError) as em:
        CustomPasswordChangeSerializer(context={"request": request})
    assert NO_USER_IN_REQUEST_MESSAGE == em.value.args[0]
