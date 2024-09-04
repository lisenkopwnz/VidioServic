from django.contrib.auth import get_user_model
from django.db import models

from content.model_content import Content


class Comment:
    comment = models.TextField(verbose_name='Коментарий')
    content = models.ForeignKey(Content, related_name='comments', on_delete=models.CASCADE)
    pub_date_time = models.DateTimeField(verbose_name="Дата и время публикации комментария", auto_now_add=True)
    author_comment = models.ForeignKey(get_user_model,on_delete=models.CASCADE,related_name='author')

    def __str__(self):
        return f'{self.comment}'

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"
