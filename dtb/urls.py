import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from codes.views import upload_unique_gift_codes_view


urlpatterns = [
    path("", lambda request: redirect("admin/")),
    path(
        "upload_unique_gift_codes/", upload_unique_gift_codes_view, name="upload_unique_gift_codes"
    ),
    path("admin/", admin.site.urls),
    path("__debug__/", include(debug_toolbar.urls)),
]
