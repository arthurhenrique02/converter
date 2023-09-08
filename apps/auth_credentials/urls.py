from django.urls import include, path
from rest_framework import routers

from apps.auth_credentials.api.viewsets import LoginViewSet

# router
router = routers.DefaultRouter()

# register router
router.register("", LoginViewSet, basename="login")

urlpatterns = [
    # add to path
    path("", include(router.urls)),
]
