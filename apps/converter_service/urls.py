from django.urls import include, path
from rest_framework import routers

from .api.viewsets import UploadViewSet

# create a router
router = routers.DefaultRouter()

router.register("upload", UploadViewSet, basename="upload")

urlpatterns = [
    # add to path
    path("", include(router.urls)),
]
