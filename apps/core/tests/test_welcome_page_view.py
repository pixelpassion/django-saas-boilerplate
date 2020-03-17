from apps.core.views import WelcomePageView


def test_welcome_view_get_context_data(settings):
    """Test that get_context_data in WelcomePageView correctly returns context."""
    settings.APP_NAME = "app_name"
    settings.SENTRY_DSN = None
    settings.API_URL = None
    settings.PUBLIC_API_DOCUMENTATION = None
    view = WelcomePageView()
    context = view.get_context_data()
    assert "APP_NAME" in context
    for name in ["API_URL", "SENTRY_DSN", "PUBLIC_API_DOCUMENTATION", "DEBUG"]:
        assert name not in context


def test_welcome_page_view_integration_test(client, settings):
    """Assert that anonymous client can access WelcomePageView and that
    welcome.html used as a template"""
    settings.STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
    response = client.get("")
    assert response.status_code == 200
    assert "welcome.html" in (t.name for t in response.templates)
