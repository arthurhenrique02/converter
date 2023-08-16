from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # add Login to path
    path("login/", include("apps.auth_credentials.urls")),
]
