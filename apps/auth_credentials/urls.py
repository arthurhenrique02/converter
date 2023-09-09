from django.urls import include, path
from rest_framework import routers

from apps.auth_credentials.api.viewsets import (CreateUserViewSet,
                                                LoginViewSet, LogoutViewSet)

# router
router = routers.DefaultRouter()

# register router
router.register("login", LoginViewSet, basename="login")
router.register("logout", LogoutViewSet, basename="logout")
router.register("register-user", CreateUserViewSet, basename="register")

urlpatterns = [
    # add to path
    path("", include(router.urls)),
]
