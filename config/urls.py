from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.views import CustomTokenObtainPairView 
from core.views import MasterListView
from rest_framework_simplejwt.views import TokenRefreshView
from core.views import UserProfileView


urlpatterns = [
    path("admin/", admin.site.urls),
    # Авторизация через JWT
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Автоматическая документация API (Swagger)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Модули системы
    path("api/applications/", include("applications.urls")),
    path("api/news/", include("news.urls")),
    path("api/notifications/", include("notifications.urls")),
    path('api/users/masters/', MasterListView.as_view(), name='master-list'),
    path('api/users/profile/', UserProfileView.as_view(), name='user-profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
