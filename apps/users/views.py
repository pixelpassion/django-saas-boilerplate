from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView

from apps.core.custom_email_backend import SaasyEmailMessage

from .models import User
from .serializers import (
    MyTokenObtainPairSerializer,
    MyTokenVerifySerializer,
    UserDetailSerializer,
    UserRegistrationSerializer,
)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyTokenVerifyView(TokenVerifyView):
    serializer_class = MyTokenVerifySerializer


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
            email_message = SaasyEmailMessage(
                template="activate-account",
                context={"link": "link"},
                to=[self.request.data["email"]],
            )
            email_message.send()
            return Response(serializer.data, status=201)
        return Response(serializer.data)


class UserApiView(ReadOnlyModelViewSet):
    serializer_class = UserDetailSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        return self.request.user
