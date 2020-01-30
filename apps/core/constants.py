from django.utils.translation import ugettext_lazy as _

SAASY_API_KEY_NOT_ASSIGNED_MESSAGE = _(
    "Set the SAASY_API_KEY in the project settings for using CustomEmailBackend"
)
INVALID_EMAIL_CLASS_USED_MESSAGE = _(
    "To use saasy you should use SaasyEmailMessage,"
    " not standard django one. "
    "Make sure you specify the 'context' and 'template' arguments"
    " when creating the email object."
)
INVALID_ARG_TYPE_MESSAGE = _('"{}" argument must be a {}')
