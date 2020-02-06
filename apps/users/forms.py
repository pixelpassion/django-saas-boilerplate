from django.contrib.auth.forms import PasswordResetForm

from apps.core.custom_email_backend import SaasyEmailMessage
from apps.users.models import User


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
            email_message = SaasyEmailMessage(
                template="reset-password", context={"link": "link"}, to=[user.email]
            )
            email_message.send()
