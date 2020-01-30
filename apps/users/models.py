import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    """
    Set User model.

    This model is inherited from default user model.
    """

    email = models.EmailField(_("Email address"), unique=True)
    privacy_policy = models.BooleanField(_("Privacy policy accepted"), default=True)
    security_hash = models.UUIDField(
        _("Security hash"), default=uuid.uuid4, unique=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        """
        Meta class of Users model.

        This class set verbose_name and verbose_name_plural.
        """

        ordering = ["date_joined"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        app_label = "users"

    def __str__(self):
        """
        __str__ method.

        This method return annotation of object.
        """
        return self.email
