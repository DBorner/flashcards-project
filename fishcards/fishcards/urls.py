from ast import pattern
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += pattern(
    "",
    (
        r"^static/(?P<path>.*)$",
        "django.views.static.serve",
        {"document_root": settings.STATIC_ROOT},
    ),
)

urlpatterns += pattern(
    "",
    (
        r"^media/(?P<path>.*)$",
        "django.views.static.serve",
        {"document_root": settings.MEDIA_ROOT},
    ),
)
