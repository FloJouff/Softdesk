from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
]
