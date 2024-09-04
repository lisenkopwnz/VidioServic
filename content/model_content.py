from django.contrib.auth import get_user_model
from django.db import models

from content.model_category import Category
from content.services import slug_generation


class Content(models.Model):
    title = models.CharField(verbose_name="Название видеоматериала", max_length=200, db_index=True)
    content = models.FileField(verbose_name="Видеоконтент", upload_to='content/$Y/%m/%d/')
    description = models.TextField(verbose_name="Описание", default=None, null=True, blank=True)
    slug = models.SlugField(verbose_name="Уникальный идндефикатор", max_length=150, unique=True, db_index=True,
                            blank=False, null=False)
    pub_date_time = models.DateTimeField(verbose_name="Дата и время публикации", auto_now_add=True)
    categories_content = models.ManyToManyField(Category, related_name='categories', null=True, blank=True)
    author_content = models.OneToOneField(get_user_model, on_delete=models.CASCADE, related_name="author")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"

    def save(self, *args, **kwargs):
        """ Переопределяем метод save из базового класса модель для автоиатического добавления slug"""
        if not self.slug:
            self.slug = slug_generation(size_slug=150)
        super().save(*args, **kwargs)
