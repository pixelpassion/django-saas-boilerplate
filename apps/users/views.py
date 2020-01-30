from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import User
from .serializers import UserDetailSerializer


class UserApiView(ReadOnlyModelViewSet):
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        return self.request.user
