from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin):
    """
    Кастомная админка для модели User, которая предоставляет дополнительные
    функции управления пользователями в Django admin.

    Параметры отображения включают поля для работы с базовой информацией пользователя,
    разрешениями, важными датами, и фильтрами для упрощения поиска и фильтрации.
    """

    fieldsets = (
        (
            None,
            {
                "fields": ("username", "email", "telephone"),
                "description": "Основные поля пользователя."
            }
        ),
        (_('Personal Info'),
         {
            "fields": ("first_name", "last_name"),
            "description": "Информация о личных данных пользователя."
         }),
        (_('Permissions'),
         {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            "description": "Поля для управления правами доступа пользователя."
        }),
        (_('Impossible change fields'),
         {
            "fields": ("last_login", "created_at"),
            "description": "Информация о последних действиях и дате создания пользователя."
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),)
    
    list_display = ("id", "get_full_name", "email", "telephone",)
    """
    Определяет, какие поля будут отображены в списке пользователей в админке.
    """
    
    list_display_links = ("id", "get_full_name",)
    """
    Устанавливает, какие поля в списке пользователей будут ссылками для перехода на страницу редактирования.
    """
    
    list_filter = ("is_staff", "is_superuser", "is_active",)
    """
    Добавляет фильтры по статусам пользователей для быстрого поиска и фильтрации в админке.
    """
    
    search_fields = ("first_name", "last_name", "email", "phone_number",)
    """
    Определяет поля, по которым можно осуществлять поиск пользователей в админке.
    """
    
    ordering = ("-id", "last_login", "created_at",)
    """
    Определяет порядок сортировки пользователей в списке. Сначала сортировка по ID в убывающем порядке.
    """
    
    filter_horizontal = ("groups", "user_permissions",)
    """
    Добавляет горизонтальные фильтры для выбора групп и разрешений пользователей.
    """
    
    readonly_fields = ("last_login", "created_at",)
    """
    Устанавливает поля 'last_login' и 'created_at' как только для чтения, чтобы их нельзя было изменить в админке.
    """