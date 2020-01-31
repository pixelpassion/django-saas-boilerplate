from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder

from rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_encode_handler

from .constants.messages import (
    EXPIRED_LINK_MESSAGE,
    REQUIRED_FLAG_MESSAGE,
    UNIQUE_EMAIL_MESSAGE,
)
from .custom_jwt import custom_jwt_payload_handler
from .forms import CustomPasswordResetForm
from .models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER


class CustomPasswordResetSerializer(PasswordResetSerializer):
    """
    Default serializer was customized to change form class
    """

    password_reset_form_class = CustomPasswordResetForm


class CustomPasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    new_password = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs["uid"]))
            self.user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError(EXPIRED_LINK_MESSAGE)

        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user,
            data={
                "new_password1": attrs["new_password"],
                "new_password2": attrs["new_password"],
            },
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs["token"]):
            raise serializers.ValidationError(EXPIRED_LINK_MESSAGE)
        return attrs

    def save(self):
        return self.set_password_form.save()


class BaseUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ["email"]

    def validate_email(self, data: str) -> str:
        data = data.lower()
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError(UNIQUE_EMAIL_MESSAGE)
        return data


class UserDetailSerializer(BaseUserSerializer):
    first_name = serializers.CharField(max_length=256, required=False)
    last_name = serializers.CharField(max_length=256, required=False)
    email = serializers.EmailField(read_only=True)
    admin_url = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + [
            "first_name",
            "last_name",
            "admin_url",
        ]

    def get_admin_url(self, instance):
        if instance.is_staff or instance.is_superuser:
            return settings.ADMIN_URL
        return None


class UserRegistrationSerializer(BaseUserSerializer):
    """ User registration serializer
    """

    token = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.CharField(max_length=256, required=True)
    last_name = serializers.CharField(max_length=256, required=True)
    password = serializers.CharField(write_only=True)
    privacy_policy = serializers.BooleanField(required=True, write_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + [
            "token",
            "first_name",
            "last_name",
            "password",
            "privacy_policy",
        ]

    def get_token(self, obj: User) -> str:
        payload = custom_jwt_payload_handler(obj)
        return jwt_encode_handler(payload)

    def validate_privacy_policy(self, data: bool) -> bool:
        if not data:
            raise serializers.ValidationError(REQUIRED_FLAG_MESSAGE)
        return data

    def validate_password(self, data: str) -> str:
        validate_password(data)
        return data

    def create(self, validated_data):
        email = validated_data.get("email")
        user = User.objects.create(
            **{
                "privacy_policy": validated_data.get("privacy_policy"),
                "first_name": validated_data.get("first_name"),
                "last_name": validated_data.get("last_name"),
                "email": email,
                "username": email,
                "is_active": False,
            }
        )
        user.set_password(validated_data.get("password"))
        user.save()
        return user


class CustomPasswordChangeSerializer(serializers.Serializer):
    """ Customized serializer for changing user password
    """

    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)

    set_password_form_class = PasswordChangeForm

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeSerializer, self).__init__(*args, **kwargs)

        self.request = self.context.get("request")
        self.user = getattr(self.request, "user", None)

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user,
            data={
                "old_password": attrs["old_password"],
                "new_password1": attrs["new_password"],
                "new_password2": attrs["new_password"],
            },
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        update_session_auth_hash(self.request, self.user)
