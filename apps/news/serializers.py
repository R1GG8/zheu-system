from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(
        source="author.full_name", default="Администрация"
    )

    class Meta:
        model = News
        fields = ["id", "title", "content", "image", "author_name", "created_at"]
