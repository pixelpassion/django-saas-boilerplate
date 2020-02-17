from datetime import timedelta

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from trench.views.simplejwt import (
    JSONWebTokenLoginOrRequestMFACode,
    JSONWebTokenLoginWithMFACode,
)

from apps.users.constants.messages import USER_ACCOUNT_INFO_HAS_ALREADY_BEEN_SENT
from apps.users.email_service import UsersSaasyEmailService

from .models import User
from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    CustomTokenVerifySerializer,
    UserDetailSerializer,
    UserRegistrationSerializer,
)


class BaseMyTokenObtainPairView:
    def handle_user_login(self, request, serializer, *args, **kwargs):
        # soft user undeletion and send recovery email
        if request.user and isinstance(request.user, User):
            user = request.user
        else:
            user = User.objects.get(email=self.request.data["email"])
        if user.is_deleted:
            user.soft_undelete_user()
            UsersSaasyEmailService().send_account_was_recovered_email(user)

        token = RefreshToken.for_user(serializer.user)
        token["security_hash"] = str(user.security_hash)
        return Response({"refresh": str(token), "access": str(token.access_token)})


class MyTokenObtainPairView(
    BaseMyTokenObtainPairView, JSONWebTokenLoginOrRequestMFACode
):
    serializer_class = CustomTokenObtainPairSerializer


class MyTokenObtainPairViewWithMFA(
    BaseMyTokenObtainPairView, JSONWebTokenLoginWithMFACode
):
    ...


class MyTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class UserRegistrationView(APIView):
    """ Default User view
    """

    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def post(self, request):
        """ Creates User
        """
        serializer = UserRegistrationSerializer(
            data=request.data, context={"request": self.request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = User.objects.get(email=self.request.data["email"])
            UsersSaasyEmailService().send_user_account_activation_email(user)
            return Response(serializer.data, status=201)
        return Response(serializer.data)


class UserApiView(ModelViewSet):
    serializer_class = UserDetailSerializer
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        return self.request.user

    def perform_destroy(self, request, format=None):
        user = self.get_object()
        user.soft_delete_user()
        if settings.ACCOUNT_DELETION_RETENTION_IN_DAYS == 0:
            user.delete()
            UsersSaasyEmailService().send_account_was_deleted_email(user)
        else:
            UsersSaasyEmailService().send_account_scheduled_for_deletion_email(user)
        return Response(status=204)


class UserAccountDataView(APIView):
    http_method_names = ["post", "get"]

    def _get_account_info_handler(self):
        import importlib

        function_string = settings.ACCOUNT_INFO_HANDLER
        mod_name, func_name = function_string.rsplit(".", 1)
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        return func

    def post(self, request, format=None):
        user = self.request.user
        if user.account_info_sent:
            return Response(status=400, data=USER_ACCOUNT_INFO_HAS_ALREADY_BEEN_SENT)
        UsersSaasyEmailService().send_account_info_asked_for_email(user)
        if settings.ACCOUNT_INFO_AUTOMATED:
            user.create_account_info_link()
            UsersSaasyEmailService().send_account_info_is_ready_email(user)
            user.account_info_sent = True
            user.save(update_fields=["account_info_sent"])
        return Response(status=201)

    def get(self, request, account_info_link, format=None):
        user = get_object_or_404(
            User,
            id=self.request.user.id,
            account_info_link=self.kwargs["account_info_link"],
            last_account_info_created__gt=timezone.now()
            - timedelta(days=settings.ACCOUNT_INFO_LINK_AVAILABILITY_IN_DAYS),
        )
        account_info_handler = self._get_account_info_handler()
        return Response(status=200, data=account_info_handler(user))
