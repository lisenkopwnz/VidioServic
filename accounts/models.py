from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        
        if not email:
            raise ValueError('Пользователь должен иметь электронный адрес')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_developer', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    username = models.CharField(unique=True, max_length=285, verbose_name="Ваш юзернейм")
    email = models.EmailField(unique=True, verbose_name="Ваш email")
    telephone = models.CharField(unique=True, max_length=255, verbose_name="Номер телефона")
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    is_admin = models.BooleanField(default=False, verbose_name="Администратор")
    is_content_maker = models.BooleanField(default=False, verbose_name="КонтентМейкер")
    is_moderator = models.BooleanField(default=False, verbose_name="Модератор")
    is_developer= models.BooleanField(default=False, verbose_name="Разработчик")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name}|{self.last_name}"
    
    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

