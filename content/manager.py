from django.db import models


class PersonQuerySet(models.QuerySet):

    def paid(self):
        return self.filter(is_private=True)

    def free(self):
        return self.filter(is_private=False)


class PersonManager(models.Manager):
    def get_queryset(self):
        return PersonQuerySet(self.model, using=self._db)

    def paid(self):
        return self.get_queryset().paid()

    def free(self):
        return self.get_queryset().free()
