from rest_framework import viewsets, permissions
from .models import News
from .serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [
                permissions.AllowAny()
            ]  # Новости могут видеть даже неавторизованные (по желанию)
        return [permissions.IsAdminUser()]  # Создавать может только персонал
