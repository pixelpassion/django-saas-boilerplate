from django.views.generic.base import TemplateView


class WelcomePageView(TemplateView):

    template_name = "welcome.html"
