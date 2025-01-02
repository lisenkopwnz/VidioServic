from django.contrib.auth import get_user_model
from django.db import models, transaction
from taggit.managers import TaggableManager

from content.manager import PersonManager
from content.models.model_category import Category
from content.services import slug_generation

from PIL import Image

from statistic.models import Statistic


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
                                      )
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
    tags = TaggableManager(blank=True,
                           verbose_name="теги",
                           related_name="posts")
    author_content = models.ForeignKey(get_user_model(),
                                       on_delete=models.CASCADE,
                                       related_name="author")

    objects = PersonManager()

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        """ Переопределяем метод save из базового класса модель для автоиатического добавления slug"""
        created = not self.pk

        if not self.slug:
            self.slug = slug_generation(size_slug=150)

        with transaction.atomic():
            super().save(*args, **kwargs)
            self.cropping_image()
            if created:
                Statistic.objects.create(content=self,author=self.author_content)

    def cropping_image(self):
        """
        Приводит изображение к соотношению сторон 9x12.
        """
        if not self.preview_image or not self.preview_image.name:
            return  # Если изображение отсутствует, ничего не делаем

        try:
            # Открываем изображение
            with Image.open(self.preview_image.path) as image:
                width, height = image.size

                # Вычисляем новую ширину для соотношения 9x12
                new_width = int(height * (9 / 12))

                # Изменяем размер изображения
                resized_image = image.resize((new_width, height), Image.Resampling.LANCZOS)

                # Вычисляем координаты для обрезки
                left = (new_width - height * (9 / 12)) / 2
                right = left + height * (9 / 12)

                # Обрезаем изображение
                cropped_image = resized_image.crop((left, 0, right, height))

                # Сохраняем изображение с высоким качеством
                cropped_image.save(self.preview_image.path, quality=95)

        except Exception as e:
            raise ValueError(f"Ошибка при обработке изображения: {str(e)}")
