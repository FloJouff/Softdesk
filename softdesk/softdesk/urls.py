from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from authentication.views import UserViewSet
from project.views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet


router = routers.SimpleRouter()
router.register("users", UserViewSet, basename="users")
router.register("projects", ProjectViewSet, basename="projects")
router.register("contributors", ContributorViewSet, basename="contributors")
router.register("issues", IssueViewSet, basename="issues")
router.register("comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("accounts/", include("allauth.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
]
