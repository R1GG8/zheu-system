from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    # Добавим имя автора вместо его ID для красоты
    author_name = serializers.ReadOnlyField(source='author.full_name')

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'image', 'created_at', 'author_name']