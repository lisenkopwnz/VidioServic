import logging
from datetime import datetime

import pytest
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from accounts.models import Profile
from comments.models import Comment
from common.utils.api_client.request_builder import HttpxClientBuilder
from content.models.model_category import Category
from content.models.model_content import Content

logger = logging.getLogger('duration_request_view')

"""
Модуль `conftest.py` содержит фикстуры для тестирования приложений Django.

Фикстуры используются для создания тестовых данных и объектов, которые могут быть
переиспользованы в различных тестах. Этот модуль автоматически обнаруживается pytest
и делает фикстуры доступными для всех тестов в проекте.

Фикстуры:
    - `create_models`: Создает тестовые модели в базе данных.
    - `request_builder`: Создает объект для выполнения HTTP-запросов.
"""

@pytest.fixture
def create_models(db):
    video = b'fake_video'
    video_file = ContentFile(video, name='video.mp4')

    user = get_user_model().objects.create(
        username='test_user',
        email='test@example.com',
        password='test_passwor123'
    )
    profile = Profile.objects.create(
        user=user,
        description='test_description',
        country='RU'
    )
    category = Category.objects.create(name='test_category')
    content = Content.objects.create(
        title='Film',
        content=video_file,
        description='description_film',
        pub_date_time=datetime.now(),
        author_content=user
    )
    comment = Comment.objects.create(
        comment='текст коммента',
        content=content,
        pub_date_time=datetime.now(),
        author_comment=user
    )

    content.categories_content.add(category)
    content.tags.add("django", "python", "testing")

    yield {
        'user': user,
        'profile': profile,
        'category': category,
        'content': content,
        'comment': comment,
    }

@pytest.fixture
def request_builder():
    """ Создаем обект запроса"""
    request = HttpxClientBuilder(
        base_url="https://api.example.com",
        timeout_connect=5,
        timeout_read=10,
        timeout_write=10,
        timeout_pool=10,
        verify_ssl=True,
    )
    return request
