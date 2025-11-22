from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)

# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="WorkZone API",
        default_version='v1',
        description="A comprehensive job portal API for connecting employers and job seekers",
        terms_of_service="https://www.workzone.com/terms/",
        contact=openapi.Contact(email="support@workzone.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/', include('jobs.urls')),
    path('api/', include('users.urls')),

    path('api/token', TokenObtainPairView.as_view(), name = 'token_obtain_pair' ),
    path('api/token/refresh', TokenRefreshView.as_view(), name = 'token_refresh'),

    # Swagger Documentation URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


