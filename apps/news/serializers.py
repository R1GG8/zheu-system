from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    # Добавим обработку автора, чтобы не было ошибки, если автор не указан
    author_name = serializers.ReadOnlyField(
        source="author.full_name", default="Администрация"
    )

    class Meta:
        model = News
        fields = ["id", "title", "content", "image", "author_name", "created_at"]
