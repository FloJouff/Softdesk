from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from project.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from project.models import Project, Contributor, Issue, Comment
from authentication.models import User


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Project to be created, viewed, edited or deleted.
    """

    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Project.objects.all()

    def perform_update(self, serializer):
        instance = serializer.save()
        new_contributors = self.request.data.get("contributors", [])

        if isinstance(new_contributors, str):
            new_contributors = [new_contributors]

        if not isinstance(new_contributors, list):
            raise ValidationError("Contributors should be a list of usernames.")

        for username in new_contributors:
            try:
                user = User.objects.get(username=username)
                if user not in instance.contributors.all():
                    instance.contributors.add(user)
            except User.DoesNotExist:
                raise ValidationError(f"User with username '{username}' does not exist.")


class ContributorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Contributor to be created, viewed, edited or deleted.
    """

    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.all()


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
