import uuid
from django.db import models
from core.models import User


class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст новости")
    image = models.ImageField(
        upload_to="news/%Y/%m/", blank=True, null=True, verbose_name="Изображение"
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name="Автор"
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
