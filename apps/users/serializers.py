from django.conf import settings

from rest_framework import serializers

from .models import User


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "admin_url",
            "is_staff",
            "is_superuser",
        ]

    def get_admin_url(self, instance):
        if instance.is_staff:
            return settings.ADMIN_URL
