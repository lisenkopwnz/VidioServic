from django.contrib.auth import get_user_model
from django.db import models

from content.models.model_content import Content
from statistic.services import SignificanceRating


class Statistic(models.Model):
    """
           Модель представляющая статистике контента пользователей приложения.

           Атрибуты:
               id (int): Уникальный идентификатор пользователя добовляется DJANGO автоматически
               content (Content): Ссылка на id контента, внешний ключ модели Content
               author_content (get_user_model): id Автора контента, , внешний ключ модели get_user_model
               number_of_likes (int): Количество лайков
               number_of_dislikes (int): Количество дизлайков
               number_of_comments (int): Количество комментариев
               number_of_views (int): Количество просмотров
           """
    content = models.OneToOneField(Content, on_delete=models.CASCADE, primary_key=True,
                                   related_name='content_statistic',
                                   verbose_name='Видиоконтент')
    author = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='author_content',
                                  verbose_name='Автор')
    number_of_likes = models.PositiveIntegerField(default=0, verbose_name='Количество лайков')
    number_of_dislikes = models.PositiveIntegerField(default=0, verbose_name='Количество дизлайков')
    number_of_comments = models.PositiveIntegerField(default=0, verbose_name='Количество комментариев')
    number_of_views = models.PositiveBigIntegerField(default=0, verbose_name='Количество просмотров')
    __rating_content = None

    @property
    def rating(self):
        """Рейтинг вкдючает лайки, дизлайки, коментарии и просмотры"""

        if self.__rating_content is None:
            self.__rating_content = SignificanceRating(self.number_of_likes,
                                                       self.number_of_dislikes,
                                                       self.number_of_comments,
                                                       self.number_of_views)
        else:
            self.__rating_content.reset(
                likes=self.number_of_likes,
                dislikes=self.number_of_dislikes,
                comments=self.number_of_comments,
                views=self.number_of_views
            )
        return self.__rating_content.calculate()

    def __str__(self):
        return f'{self.content}'

    class Meta:
        verbose_name = "Cтатистика"
        verbose_name_plural = "Cтатистика"
