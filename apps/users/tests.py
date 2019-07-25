from .models import User


def test_user_str_method():
    assert str(User(email="email@email.com")) == "email@email.com"
