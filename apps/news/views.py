from rest_framework import generics, permissions
from .models import News
from .serializers import NewsSerializer

class NewsListView(generics.ListAPIView):
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer
    # Вот здесь мы ограничиваем доступ:
    permission_classes = [permissions.IsAuthenticated]