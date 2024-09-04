from django.db import models


class Category(models.Model):
    name = title = models.CharField(verbose_name="Название категории", max_length=200, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Котегория"
        verbose_name_plural = "Котегории"
