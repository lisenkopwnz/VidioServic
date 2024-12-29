from datetime import datetime
from typing import Any

import pytest
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from comments.models import Comment
from content.models.model_category import Category
from content.models.model_content import Content


class TestModelsStatistic:

    @pytest.fixture
    def create_fake_video(self) -> ContentFile:
        """ Создаем фикстуру ,которая будет создовать фейковый файл для поля content
            модели Content"""
        video_content = b'Video content'

        # Создаем ContentFile с заданным именем
        video_file = ContentFile(video_content, name='video.mp4')

        # Возвращаем объект ContentFile
        return video_file

    @pytest.fixture
    def create_models(self, create_fake_video, db: Any) -> None:
        """ Создаем экземпляры модели Category, Content, get_user_model, Comment"""
        user_object = get_user_model().objects.create_user(username='test_user',
                                                           email='test@example.com',
                                                           password='test_passwor123')
        category_object = Category.objects.create(name='Sport')
        content_object = Content.objects.create(title='Film',
                                                content=create_fake_video,
                                                description='description_film',
                                                pub_date_time=datetime.now(),
                                                author_content=user_object)

        content_object.categories_content.add(category_object)

        return Comment.objects.create(comment='test_comment',
                                      content=content_object,
                                      pub_date_time=datetime.now(),
                                      author_comment=user_object)

    def test_foreign_keys(self, create_models: Comment) -> None:
        """ Проверяем внешние ключи """
        assert str(create_models.author_comment) == 'test_user'
        assert str(create_models.content) == 'Film'

    def test_update_category(self, create_models: Comment) -> None:
        """ Проверяем экземпляр модели Comment на предмет изменения"""
        create_models.comment = 'test_comment_update'
        create_models.save()
        update_comment = Comment.objects.get(comment='test_comment_update')
        assert update_comment.comment == 'test_comment_update'
