from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    Group, Permission
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from accounts.managers.user_manager import UserManager
from django.utils import timezone


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
        last_login (DateTimeField): Дата и время последнего входа пользователя. Устанавливается автоматически при входе.

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

    last_login = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата последнего входа",
        null=True
    )

    user_role = models.CharField(
        max_length=3,
        choices=Role.choices,
        default=Role.CUSTOMER,
        verbose_name='Роль | Пользователя'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Статус персонала"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Уникальное имя для групп
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Уникальное имя для разрешений
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    class Meta:
        app_label = 'accounts'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def get_full_name(self):
        return f"{self.first_name}|{self.last_name}"

    def __str__(self):
        return f'{self.get_full_name} | {self.pk}'
