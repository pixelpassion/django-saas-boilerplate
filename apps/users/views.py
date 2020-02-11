from django.conf import settings

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
