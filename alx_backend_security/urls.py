from django.contrib import admin
from django.urls import path
from ip_tracking import views

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Backend Security API",
        default_version='v1',
        description="API documentation for alx-backend-security",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('anon/', views.anonymous_view),
    path('auth/', views.authenticated_view),

    # Swagger endpoint
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
