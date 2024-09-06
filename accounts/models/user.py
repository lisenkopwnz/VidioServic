from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from accounts.managers.user import UserManager
from django.contrib.auth.models import (
                                        AbstractBaseUser,
                                        PermissionsMixin,
                                        )



class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя, которая расширяет базовые классы AbstractBaseUser и PermissionsMixin Django.

    Данная модель представляет пользователя в системе и содержит несколько ключевых полей для хранения 
    информации о пользователе, таких как юзернейм, email и номер телефона. Также включает поля для 
    отслеживания времени последнего входа, даты создания и даты изменения учетной записи.

    Атрибуты:
        username (CharField): Уникальный юзернейм пользователя.
        first_name (CharField): Имя пользователя. Необязательное поле.
        second_name (CharField): Фамилия пользователя. Необязательное поле.
        email (EmailField): Уникальный email пользователя.
        telephone (PhoneNumberField): Уникальный номер телефона пользователя. Необязательное поле.
        created_at (DateTimeField): Дата создания учетной записи. Устанавливается по умолчанию на текущее время.

    Методы:
            objects (UserManager): Пользовательский менеджер для управления учетными записями.
    """

    class Role(models.TextChoices):
        CUSTOMER = 'CUS', _('Клиент')
        ADMIN = 'ADM', _('Админимстратор')
        MODERATOR = 'MOD', _('Модератор')
        CONTENT_MAKER = 'CNM', _('КонетнтМейкер')
        DEVELOPER = 'DEV', _('Разработчик')


    username = models.CharField(
        unique=True,
        max_length=285, 
        verbose_name="Ваш юзернейм"
    )
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True, 
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Фамилия"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Ваш email"
    )
    telephone = PhoneNumberField(
        unique=True, 
        verbose_name="Номер телефона",
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата создания"
    )

    user_role = models.CharField(
        max_length = 3, 
        choices=Role.choices,
        default=Role.CUSTOMER, 
        verbose_name='Роль | Пользователя'
    )

    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'User'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property    
    def get_full_name(self):
            return f"{self.first_name}|{self.last_name}"
    
    def __str__(self):
        return f'{self.get_full_name} | {self.pk}'
    
    
    
   