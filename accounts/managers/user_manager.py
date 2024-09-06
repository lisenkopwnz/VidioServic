from django.contrib.auth.models import BaseUserManager
# from django.contrib.auth import get_user_model
from typing import Union, Optional
from rest_framework.exceptions import ParseError


# User = get_user_model()

from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    @staticmethod
    def __check_email_or_phone_number(
        email: str, 
        phone_number: str
    ) -> Optional[str]:
        return email or phone_number
    
    def _create_user(
        self, 
        phone_number: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        username: Optional[str] = None, 
        **extra_fields: Optional[str]
    ): # type: ignore
        if not (email and username):
            raise ValidationError('Заполните поля email и username для входа в систему')

        # Нормализация email
        email = self.normalize_email(email)

        # Проверка, существует ли пользователь с таким email
        if self.model.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')

        user = self.model(username=username, email=email, **extra_fields)

        if phone_number:
            user.phone_number = phone_number
        if user.is_superuser:
            user.role = user.Role.ADMIN

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(
        self, 
        phone_number: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        username: Optional[str] = None, 
        **extra_fields: Union[str, bool]
    ): # type: ignore
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )
    
    def create_superuser(
        self, 
        phone_number: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        username: Optional[str] = None, 
        **extra_fields: Union[str, bool]
    ): # type: ignore
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError('Поле is_superuser должно быть установлено в True')

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )
