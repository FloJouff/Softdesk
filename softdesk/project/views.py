from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from project.serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ContributorSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    CommentSerializer,
)
from project.models import Project, Contributor, Issue, Comment
from authentication.models import User
from project.permissions import (
    IsAuthorOrAssignee,
    IsAuthorOrReadOnlyForContributorsProject,
    IsProjectContributor_Comment,
    IsProjectContributor_Issue,
)


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows Project to be created, viewed, edited or deleted.
    """

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnlyForContributorsProject]

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


class IssueViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows Issues to be created, viewed, edited or deleted.
    """

    queryset = Issue.objects.all()
    serializer_class = IssueListSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrAssignee, IsProjectContributor_Issue]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return IssueListSerializer
        return IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.filter(project__contributors=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet, MultipleSerializerMixin):
    """
    API endpoint that allows Comments to be created, viewed, edited or deleted.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor_Comment]

    def get_queryset(self):
        return Comment.objects.filter(issue__project__contributors=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
