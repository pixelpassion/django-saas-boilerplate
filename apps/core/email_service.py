from apps.core.custom_email_backend import SaasyEmailMessage


class BaseSaasyEmailService:
    def _send_message(self, email, template_name, context={}):
        email_message = SaasyEmailMessage(
            template=template_name, context=context, to=[email]
        )
        email_message.send()
