from rest_framework import viewsets
from rest_framework.response import Response

from authentication.serializers import UserSerializer
from authentication.models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
