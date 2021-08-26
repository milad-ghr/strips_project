from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import permissions, authentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Strips API Service",
        default_version='v1',
        license=openapi.License(name="Milad Ghr License"),
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
    authentication_classes=(authentication.BasicAuthentication,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include('users.urls')),
    path("payments/", include('payments.urls')),
    path("products/", include('products.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
