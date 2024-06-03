from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from authentication.views import UserViewSet


router = routers.SimpleRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("accounts/", include("allauth.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
]
