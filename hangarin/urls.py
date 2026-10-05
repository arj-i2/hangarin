from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("tasks.urls")),
    path("pwa/", include(("pwa.urls", "pwa"), namespace="pwa")),
]