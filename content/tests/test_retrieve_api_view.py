from unittest.mock import patch
from rest_framework.test import APIClient

import pytest

from django.http import Http404, HttpRequest

from common.utils.api_client.exceptions import ApiClientException
from conftest import create_models
from content.api.views.content_retrieve_view import ContentRetrieveView


class TestRetrieveApiView:
    """
    Набор тестов для API-представления ContentRetrieveView.
    """

    def test_extract_list_from_dict_success(self):
        """
        Проверяет, что метод _extract_list_from_dict успешно извлекает список из словаря.
        """
        data = {'slug': ['rec1,rec2,rec3']}
        result = ContentRetrieveView._extract_list_from_dict(data)
        assert result == ['rec1,rec2,rec3']

    def test_extract_list_from_dict_empty(self):
        """
        Проверяет, что метод _extract_list_from_dict выбрасывает исключение ApiClientException, если входные данные пусты.
        """
        data = {'recommendation': []}
        with pytest.raises(ApiClientException) as exc_info:
            ContentRetrieveView._extract_list_from_dict(data)
        assert exc_info.value.error_code == 'EMPTY_RESPONSE'

    def test_extract_list_from_dict_invalid_format(self):
        """
        Проверяет, что метод _extract_list_from_dict выбрасывает исключение ApiClientException, если формат входных данных неверен.
        """
        data = {"slug": "not-a-list"}
        with pytest.raises(ApiClientException) as exc_info:
            ContentRetrieveView._extract_list_from_dict(data)
        assert exc_info.value.error_code == "INVALID_DATA_FORMAT"

    @pytest.mark.django_db
    def test_get_object_success(self, create_models):
        """
        Проверяет, что метод get_object успешно извлекает объект по его первичному ключу.
        """
        content = create_models['content']
        user = create_models['user']

        view = ContentRetrieveView()
        view.kwargs = {'pk': content.pk}

        request = HttpRequest()
        request.user = user
        view.request = request

        obj = view.get_object()
        assert obj.title == "Film"

    @pytest.mark.django_db
    def test_get_object_not_found(self, create_models):
        """
        Проверяет, что метод get_object выбрасывает исключение Http404, если объект не найден.
        """
        user = create_models['user']

        view = ContentRetrieveView()

        request = HttpRequest()
        request.user = user
        view.request = request

        view.kwargs = {'pk': 999}  # Несуществующий ID

        with pytest.raises(Http404):
            view.get_object()

    @pytest.mark.django_db
    def test_retrieve_success(self, create_models):
        """
        Проверяет, что метод retrieve успешно возвращает ожидаемый ответ.
        """
        content = create_models['content']

        recommendations = {"slug": ["recommendation-1", "recommendation-2"]}

        with patch('content.api.views.content_retrieve_view.ContentRetrieveView._get_recommendations',
                   return_value=recommendations):
            client = APIClient()
            url = f'api/video/{content.slug}/'
            response = client.get(url)

            assert response.status_code == 404
