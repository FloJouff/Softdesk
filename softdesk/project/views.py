from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from project.serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ContributorSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    IssueCreateUpdateSerializer,
    CommentSerializer,
)
from project.models import Project, Contributor, Issue, Comment
from authentication.models import User
from project.permissions import (
    IsAuthorOrReadOnlyForContributorsProject,
    IsProjectContributor_Comment,
    IsProjectContributor_Issue,
)


class MultipleSerializerMixin:

    detail_serializer_class = None
    create_update_serializer_class = None

    def get_serializer_class(self):
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        if self.action in ["create", "update", "partial_update"] and self.create_update_serializer_class is not None:
            return self.create_update_serializer_class
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
    API endpoint that allows Contributor to be added or viewed.
    """
    queryset = User.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnlyForContributorsProject]

    def get_queryset(self):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        return project.contributors.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project"] = Project.objects.get(pk=self.kwargs["project_pk"])
        return context

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        self.check_object_permissions(request, project)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        project.contributors.add(user)
        return Response({"status": "contributor added", "username": user.username}, status=status.HTTP_201_CREATED)

    @action(
        detail=False, methods=["post"], permission_classes=[IsAuthenticated, IsAuthorOrReadOnlyForContributorsProject]
    )
    def add_contributor(self, request, project_pk=None):
        project = get_object_or_404(Project, pk=project_pk)
        self.check_object_permissions(request, project)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        project.contributors.add(user)
        return Response({"status": "contributor added", "username": user.username}, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["delete"],
        url_path="remove_contributor",
        permission_classes=[IsAuthenticated, IsAuthorOrReadOnlyForContributorsProject],
    )
    def remove_contributor(self, request, project_pk=None, pk=None):
        project = get_object_or_404(Project, pk=project_pk)
        self.check_object_permissions(request, project)
        user = get_object_or_404(User, pk=pk)
        if user in project.contributors.all():
            project.contributors.remove(user)
            return Response(
                {"status": "contributor removed", "username": user.username}, status=status.HTTP_204_NO_CONTENT
            )
        return Response({"status": "user not a contributor"}, status=status.HTTP_400_BAD_REQUEST)


class IssueViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows Issues to be created, viewed, edited or deleted.
    """

    queryset = Issue.objects.all()
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    create_update_serializer_class = IssueCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor_Issue]

    def get_serializer_class(self):
        if self.action in ["list"]:
            return IssueListSerializer
        if self.action in ["retrieve"]:
            return IssueDetailSerializer
        if self.action in ["create", "update", "partial_update"]:
            return IssueCreateUpdateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(viewsets.ModelViewSet, MultipleSerializerMixin):
    """
    API endpoint that allows Comments to be created, viewed, edited or deleted.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor_Comment]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs["issue_pk"])

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs["issue_pk"])
        serializer.save(author=self.request.user, issue=issue)
