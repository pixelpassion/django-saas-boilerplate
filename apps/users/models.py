import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from .constants.messages import (
    USER_ALREADY_DELETED_MESSAGE,
    USER_WILL_BE_DELETED_MESSAGE,
)


class User(AbstractUser):
    """
    Set User model.

    This model is inherited from default user model.
    """

    NO_WARNING, FIRST_WARNING_SENT, SECOND_WARNING_SENT = (
        "no_warnings",
        "first_warning_sent",
        "second_warning_sent",
    )
    WARNING_CHOICES = (
        (NO_WARNING, _("No warnings")),
        (FIRST_WARNING_SENT, _("First warning sent")),
        (SECOND_WARNING_SENT, _("Second warning sent")),
    )

    email = models.EmailField(_("Email address"), unique=True)
    privacy_policy = models.BooleanField(_("Privacy policy accepted"), default=True)
    security_hash = models.UUIDField(
        _("Security hash"), default=uuid.uuid4, unique=True
    )
    is_deleted = models.BooleanField(_("Deleted"), default=False)
    warning_sent_email = models.CharField(
        verbose_name=_("Warning email"),
        choices=WARNING_CHOICES,
        max_length=256,
        default=NO_WARNING,
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

    def soft_undelete_user(self):
        if self.last_login > timezone.now() - timedelta(
            days=settings.ACCOUNT_DELETION_RETENTION_IN_DAYS
        ):
            self.is_deleted = False
            self.save()
        else:
            raise ValidationError(USER_WILL_BE_DELETED_MESSAGE)

    def soft_delete_user(self):
        if self.is_deleted:
            raise ValidationError(USER_ALREADY_DELETED_MESSAGE)
        self.is_deleted = True
        self.last_login = timezone.now()
        self.save(update_fields=["is_deleted", "last_login"])

    def __str__(self):
        """
        __str__ method.

        This method return annotation of object.
        """
        return self.email
