from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Project


class IsAuthorOrReadOnlyForContributorsProject(BasePermission):
    """
    Custom permission to only allow authors of a project to edit or delete it,
    but allow contributors to read it.
    """
    def has_permission(self, request, view):
        project_pk = view.kwargs.get("project_pk")
        if project_pk:
            project = Project.objects.get(pk=project_pk)
            if request.method == "DELETE":
                return project.author == request.user

        return True

    def has_object_permission(self, request, view, obj):
        # Handle different types of objects that may be checked
        if isinstance(obj, Project):
            # Read permissions are allowed to any contributor of the project
            if request.method in SAFE_METHODS:
                return (request.user in obj.contributors.all()) or (request.user == obj.author)
            # Write permissions are only allowed to the author of the project
            return obj.author == request.user

        # Assuming 'obj' is a contributor (User) being removed from a project
        project_pk = view.kwargs.get("project_pk")
        if project_pk:
            project = Project.objects.get(pk=project_pk)
            if request.method == "DELETE":
                return project.author == request.user

        return False


class IsProjectContributor_Comment(BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it,
    but allow contributors, and only contributors, to read it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any contributor of the project
        if request.method in SAFE_METHODS:
            return (obj.issue.project.contributors.filter(pk=request.user.pk).exists()) or (
                obj.issue.project.author == request.user
            )
        return obj.author == request.user


class IsProjectContributor_Issue(BasePermission):
    """
    Custom permission to only allow authors of an issue to edit or delete it,
    but allow contributors, and only contributors, to read it.
    """

    def has_permission(self, request, view):
        if view.action in ["create"]:
            project_id = view.kwargs.get("project_pk")
            if project_id:
                project = Project.objects.get(pk=project_id)
                return (request.user in project.contributors.all()) or (request.user == project.author)
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any contributor of the project
        if request.method in SAFE_METHODS:
            return (request.user in obj.project.contributors.all()) or (request.user == obj.author)

        # Write permissions are only allowed to the author of the issue
        return obj.author == request.user
