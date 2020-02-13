from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder

from rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken

from .constants.messages import (
    EXPIRED_LINK_MESSAGE,
    INVALID_TOKEN_MESSAGE,
    NO_REQUEST_IN_CONTEXT_MESSAGE,
    NO_USER_IN_REQUEST_MESSAGE,
    REQUIRED_FLAG_MESSAGE,
    UNIQUE_EMAIL_MESSAGE,
)
from .forms import CustomPasswordResetForm, CustomSetPasswordForm
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ CustomTokenObtainPairSerializer is designed to add the user security_hash
        to token attributes and return additional data with token data
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["security_hash"] = str(user.security_hash)
        return token


def validate_token_by_security_hash(token: object):
    """ Сhecks if the user security_hash is equal to the security_hash from the token
    """
    user = User.objects.get(id=token["user_id"])
    if str(user.security_hash) != token["security_hash"]:
        raise serializers.ValidationError(INVALID_TOKEN_MESSAGE)
    return


class CustomTokenVerifySerializer(TokenVerifySerializer):
    """ CustomTokenVerifySerializer is designed to configure the validate
        method and verify the token by user security_hash
    """

    def validate(self, attrs):
        token = UntypedToken(attrs["token"])
        validate_token_by_security_hash(token)
        return {}


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """ CustomTokenRefreshSerializer is designed to configure the validate
        method and verify the token by user security_hash
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs["refresh"])
        validate_token_by_security_hash(refresh)
        return data


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

    set_password_form_class = CustomSetPasswordForm

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
            "last_password_change_date",
        ]

    def get_admin_url(self, instance):
        if instance.is_staff or instance.is_superuser:
            return settings.ADMIN_URL
        return None


class UserRegistrationSerializer(BaseUserSerializer):
    """ User registration serializer
    """

    access = serializers.SerializerMethodField(
        read_only=True, method_name="get_access_token"
    )
    refresh = serializers.SerializerMethodField(
        read_only=True, method_name="get_refresh_token"
    )
    first_name = serializers.CharField(max_length=256, required=True)
    last_name = serializers.CharField(max_length=256, required=True)
    password = serializers.CharField(write_only=True)
    privacy_policy = serializers.BooleanField(required=True, write_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + [
            "access",
            "refresh",
            "first_name",
            "last_name",
            "password",
            "privacy_policy",
        ]

    def get_access_token(self, user: User) -> str:
        refresh_token = RefreshToken.for_user(user)
        return str(refresh_token.access_token)

    def get_refresh_token(self, user: User) -> str:
        refresh_token = RefreshToken.for_user(user)
        return str(refresh_token)

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
            privacy_policy=validated_data.get("privacy_policy"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            email=email,
            username=email,
            is_active=False,
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
        if self.request:
            self.user = getattr(self.request, "user", None)
            if not self.user:
                raise serializers.ValidationError(NO_USER_IN_REQUEST_MESSAGE)
        else:
            raise serializers.ValidationError(NO_REQUEST_IN_CONTEXT_MESSAGE)

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
