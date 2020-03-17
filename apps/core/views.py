from django.conf import settings
from django.views.generic.base import TemplateView


class WelcomePageView(TemplateView):

    template_name = "welcome.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        for var_name in [
            "APP_NAME",
            "API_URL",
            "SENTRY_DSN",
            "PUBLIC_API_DOCUMENTATION",
            "DEBUG",
        ]:
            variable = getattr(settings, var_name, None)
            if variable:
                context[var_name] = variable
        return context
