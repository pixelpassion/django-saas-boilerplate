from datetime import timedelta

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.gdpr.email_service import SaasyEmailService

from .models import User
from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    CustomTokenVerifySerializer,
    UserDetailSerializer,
    UserRegistrationSerializer,
)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        data = super().post(request, *args, **kwargs)

        # soft user undeletion and send recovery email
        user = User.objects.get(email=self.request.data["email"])
        if user.is_deleted:
            user.soft_undelete_user()
            SaasyEmailService().send_account_was_recovered_email(user)

        return data


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
            SaasyEmailService().send_user_account_activation_email(user)
            return Response(serializer.data, status=201)
        return Response(serializer.data)


class UserApiView(ReadOnlyModelViewSet):
    serializer_class = UserDetailSerializer
    http_method_names = ["get", "delete"]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        return self.request.user

    def perform_destroy(self, request, format=None):
        user = self.get_object()
        user.soft_delete_user()
        if settings.ACCOUNT_DELETION_RETENTION_IN_DAYS == 0:
            user.delete()
            SaasyEmailService().send_account_was_deleted_email(user)
        else:
            SaasyEmailService().send_account_scheduled_for_deletion_email(user)
        return Response(status=204)


class UserAccountDataView(APIView):
    http_method_names = ["post", "get"]

    def post(self, request, format=None):
        user = self.request.user
        user.create_account_info_link()
        return Response(status=201)

    def get(self, request, account_info_link, format=None):
        user = get_object_or_404(
            User,
            id=self.request.user.id,
            account_info_link=self.kwargs["account_info_link"],
            last_account_info_created__gt=timezone.now()
            - timedelta(days=settings.ACCOUNT_INFO_LINK_AVAILABILITY_IN_DAYS),
        )
        user_data = {"email": user.email}
        return Response(status=200, data=user_data)
