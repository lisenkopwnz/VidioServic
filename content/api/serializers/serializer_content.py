from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import Profile
from comments.models import Comment
from content.models.model_category import Category
from content.models.model_content import Content
from statistic.models import Statistic


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя (`User`).
    Используется для представления данных автора контента и авторов комментариев.
    """
    class Meta:
        model = get_user_model()
        fields = ['username']


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели профиля (`Profile`).
    Используется для представления данных профиля автора контента.
    """
    class Meta:
        model = Profile
        fields = ['user_photo']


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели категории (`Category`).
    Используется для представления категорий контента.
    """
    class Meta:
        model = Category
        fields = ['name']


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели комментария (`Comment`).
    Используется для представления комментариев к контенту.
    """
    author_comment = UserSerializer()

    class Meta:
        model = Comment
        fields = ['comment', 'pub_date_time', 'author_comment']


class ContentStatisticSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели статистики (`Statistic`).
    Используется для представления статистики контента.
    """
    class Meta:
        model = Statistic
        fields = ['number_of_likes', 'number_of_dislikes', 'number_of_comments', 'number_of_views']


class ContentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели контента (`Content`).
    Используется для представления данных контента, включая связанные объекты.
    """
    author_content = UserSerializer()
    profile = ProfileSerializer(source='author_content.profile')  # Используем ProfileSerializer
    categories_content = CategorySerializer(many=True)
    comments = CommentSerializer(many=True)
    content_statistic = ContentStatisticSerializer()

    class Meta:
        model = Content
        fields = [
            'id',
            'title',
            'content',
            'description',
            'preview_image',
            'slug',
            'pub_date_time',
            'categories_content',
            'is_private',
            'author_content',
            'profile',  # Поле profile
            'comments',
            'content_statistic',
        ]