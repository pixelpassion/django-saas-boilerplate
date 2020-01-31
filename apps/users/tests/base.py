def mock_email_backend_send_messages(mocker, settings):
    settings.SAASY_API_KEY = "some_key"
    settings.EMAIL_BACKEND = "apps.core.custom_email_backend.CustomEmailBackend"
    return mocker.patch(
        f"apps.core.custom_email_backend.CustomEmailBackend.send_messages"
    )
