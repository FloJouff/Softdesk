from rest_framework import viewsets, status
from rest_framework.response import Response

from authentication.serializers import UserSerializer
from authentication.models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be created, viewed, edited or deleted.
    """

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def update(self, request, *args, **kwargs):
        if request.user.id != kwargs.get("pk"):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.id != kwargs.get("pk"):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
