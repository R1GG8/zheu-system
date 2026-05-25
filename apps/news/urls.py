from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet

# Используем роутер для автоматического создания путей (list, retrieve, create и т.д.)
router = DefaultRouter()
router.register(r"", NewsViewSet, basename="news")

urlpatterns = [
    path("", include(router.urls)),
]
