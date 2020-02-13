from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils import timezone

from .email_service import UsersSaasyEmailService
from .models import User


class CustomPasswordResetForm(PasswordResetForm):
    """
    Default form was customized to create an RefreshToken object
    during saving and update templates
    """

    def save(
        self,
        domain_override=None,
        subject_template_name=None,
        email_template_name=None,
        use_https=False,
        token_generator=None,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        user = User.objects.filter(
            email=self.cleaned_data["email"], is_active=True
        ).first()
        if user:
            UsersSaasyEmailService().send_reset_password_email(user)


class CustomSetPasswordForm(SetPasswordForm):
    def save(self, commit=True):
        super().save(commit)
        self.user.last_password_change_date = timezone.now()
        self.user.save()
        return self.user
