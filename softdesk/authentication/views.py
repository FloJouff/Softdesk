from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from authentication.serializers import UserSerializer
from authentication.models import User
from authentication.permissions import IsOwnerOrReadOnly


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be created, viewed, edited or deleted.
#     """

#     serializer_class = UserSerializer

#     def get_queryset(self):
#         return User.objects.all()

#     def update(self, request, *args, **kwargs):
#         if request.user.id != kwargs.get("pk"):
#             return Response(status=status.HTTP_403_FORBIDDEN)
#         return super().update(request, *args, **kwargs)

#     def destroy(self, request, *args, **kwargs):
#         if request.user.id != kwargs.get("pk"):
#             return Response(status=status.HTTP_403_FORBIDDEN)
#         return super().destroy(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_permissions(self):
        # Permettre à l'utilisateur de lire et mettre à jour leur propre profil
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        elif self.action == "create":
            self.permission_classes = []
        return super(UserViewSet, self).get_permissions()
