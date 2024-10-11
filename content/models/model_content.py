from django.contrib.auth import get_user_model
from django.db import models
from django.http import JsonResponse

from content.models.model_category import Category
from content.services import slug_generation

from PIL import Image


class Content(models.Model):
    """
       Модель представляющая контент пользователей приложения.

       Атрибуты:
           id (int): Уникальный идентификатор пользователя добовляется DJANGO автоматически
           title (str): Заголовок видеоконтента
           content (FileField): Видеоконтент
           preview_image (ImageField): Превью видиоконтента
           description (str): Описание видеоконтента
           slug (str): Уникальный идндефикатор видеоконтента
           pub_date_time (datetime): Дата публикации
           is_private (bool): Сделать видео приватным или публичным
           categories_content (Category): Возможные категории контента, внешний ключ модели Category
           author_content (get_user_model): id Автора контента, , внешний ключ модели get_user_model
       """
    title = models.CharField(verbose_name="Название видеоматериала",
                             max_length=200,
                             db_index=True)
    content = models.FileField(verbose_name="Видеоконтент",
                               upload_to='content/$Y/%m/%d/')
    preview_image = models.ImageField(verbose_name='Превью',
                                      upload_to='preview/$Y/%m/%d/',
                                      blank=True, null=True,
                                      default=None)
    description = models.TextField(verbose_name="Описание",
                                   default=None,
                                   null=True,
                                   blank=True)
    slug = models.SlugField(verbose_name="Уникальный идндефикатор",
                            max_length=150,
                            unique=True,
                            db_index=True,
                            blank=False,
                            null=False)
    pub_date_time = models.DateTimeField(verbose_name="Дата и время публикации",
                                         auto_now_add=True)
    is_private = models.BooleanField(verbose_name="Сделать видео приватным",
                                     choices=[(True, 'Да'), (False, 'Нет')],
                                     default=False)
    categories_content = models.ManyToManyField(Category,
                                                related_name='categories_content',
                                                blank=True)
    author_content = models.ForeignKey(get_user_model(),
                                       on_delete=models.CASCADE,
                                       related_name="author")

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        """ Переопределяем метод save из базового класса модель для автоиатического добавления slug"""
        if not self.slug:
            self.slug = slug_generation(size_slug=150)
        super().save(*args, **kwargs)

        self.cropping_image()

    def cropping_image(self):
        """Данный метод используется для приведения изображения к соотношению сторон 9x12"""

        if self.preview_image and self.preview_image.name:
            try:
                image = Image.open(self.preview_image.path)
                width, height = image.size

                new_width = int(height * (9 / 12))
                image = image.resize((new_width, height), Image.ANTIALIAS)

                left = (new_width - height * (9 / 12)) / 2
                image = image.crop((left, 0, left + height * (9 / 12), height))

                image.save(self.preview_image.path)
            except Exception as e:
                return JsonResponse({'Ошибка при обработке изображения': str(e)}, status=400)
