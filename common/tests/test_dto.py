import pytest

from common.utils.api_client.data_preparer import RecommendationDTO
from conftest import create_models


class TestRecommendationDTO:
    """
    Класс для тестирования функциональности RecommendationDTO.
    """

    @pytest.mark.django_db(transaction=True)
    def test_create(self, create_models):
        """
        Тестирует метод `create` класса RecommendationDTO.

        Проверяет, что метод корректно создаёт объект RecommendationDTO
        на основе переданного объекта Content.

        Args:
            create_models: Фикстура, создающая тестовые данные.
        """
        # Получаем объект Content из фикстуры
        content = create_models['content']

        # Создаём объект RecommendationDTO с использованием метода create
        dto = RecommendationDTO.create(content)

        # Проверяем, что возвращённый объект является экземпляром RecommendationDTO
        assert isinstance(dto, RecommendationDTO)

        # Проверяем, что поля DTO соответствуют данным из объекта Content
        assert dto.slug == content.slug
        assert dto.title == content.title
        assert dto.description == content.description
        assert dto.pub_date_time == content.pub_date_time

        # Проверяем, что rating корректно вычисляется
        if hasattr(content, 'content_statistic'):
            assert dto.rating == content.content_statistic.rating
        else:
            assert dto.rating == 0.0

        # Проверяем, что categories_content и tags корректно преобразуются
        assert dto.categories_content == list(content.categories_content.values_list('name', flat=True))
        assert dto.tags == content.tags

    @pytest.mark.django_db(transaction=True)
    def test_to_dict(self, create_models):
        """
        Тестирует метод `to_dict` класса RecommendationDTO.

        Проверяет, что метод корректно преобразует объект RecommendationDTO
        в словарь с правильной сериализацией данных.

        Args:
            create_models: Фикстура, создающая тестовые данные.
        """
        # Получаем объект Content из фикстуры
        content = create_models['content']

        # Создаём объект RecommendationDTO с использованием метода create
        dto = RecommendationDTO.create(content)

        # Преобразуем объект DTO в словарь
        dto_dict = dto.to_dict()

        # Проверяем, что результат является словарём
        assert isinstance(dto_dict, dict)

        # Проверяем, что pub_date_time преобразован в строку
        assert isinstance(dto_dict['pub_date_time'], str)

        # Проверяем, что categories_content является списком
        assert isinstance(dto_dict['categories_content'], list)
