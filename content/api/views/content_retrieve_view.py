from typing import Dict, List

from django.db.models import QuerySet, Prefetch
from django.http import Http404
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.response import Response

from comments.models import Comment
from common.utils.api_client.data_preparer import RecommendationDTO
from common.utils.api_client.exceptions import ApiClientException
from common.utils.api_client.request_sender import ContentBasedRecommendationsClient
from common.utils.common_services import user_status_subscription
from content.api.serializers.serializer_content import ContentSerializer
from content.models.model_category import Category
from content.models.model_content import Content


class ContentRetrieveView(RetrieveAPIView):
    """
    Представление для получения деталей контента и рекомендаций.

    Attributes:
        serializer_class (ContentSerializer): Сериализатор для контента.
        lookup_field (str): Поле для поиска объекта (по умолчанию 'slug').
    """
    serializer_class = ContentSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос для получения деталей контента и рекомендаций.

        Returns:
            Response: JSON-ответ с данными контента и рекомендациями.
                     В случае ошибки возвращает частичный ответ с сообщением об ошибке.

        Raises:
            ApiClientException: Если произошла ошибка при получении рекомендаций.
            Exception: Если произошла непредвиденная ошибка.
        """
        # Получаем объект контента и сериализуем его
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        try:
            # Получаем рекомендации
            recommendations = self._get_recommendations(instance)
            # Получаем список индетификаторов
            recommendations_slug = self._extract_list_from_dict(recommendations)
            # Получаем Queryset, рекомендаций
            recommendations = self._list_recommendations(recommendations_slug)
            # Сериализуем список рекомендаций
            serializer_recommendations = self.get_serializer(recommendations, many=True)

            # Формируем успешный ответ
            response_data = {
                'video': serializer.data,
                'recommendations': serializer_recommendations.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Http404:
            # Возвращаем ответ с кодом 404, если объект не найден
            return Response(
                {"detail": "Запись не найдена."},
                status=status.HTTP_404_NOT_FOUND
            )
        except ApiClientException as e:
            # Возвращаем частичный ответ с данными контента и пустыми рекомендациями
            response_data = {
                'video': serializer.data,
                'recommendations': [],
                'error': e.message,
                'error_code': e.error_code,
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self, queryset:QuerySet=None)-> Content:
        """
         Возвращает объект по `pk` с оптимизацией запросов к базе данных.
        """
        queryset = queryset or self.get_queryset()
        return get_object_or_404(
            queryset.select_related('content_statistic', 'author_content__profile')
            .prefetch_related(
                Prefetch('comments', queryset=Comment.objects.select_related('author_comment')
                         .only('comment', 'pub_date_time', 'author_comment__username')),
                Prefetch('categories_content', queryset=Category.objects.only('name'))
            )
            .only(
                'title', 'content', 'preview_image', 'description', 'slug', 'pub_date_time', 'is_private', 'tags',
                'author_content__username', 'author_content__profile__user_photo',
                'content_statistic__number_of_likes', 'content_statistic__number_of_dislikes',
                'content_statistic__number_of_comments', 'content_statistic__number_of_views',
            ),
            pk=self.kwargs['pk']
        )

    def _list_recommendations(self,list_slug:List[str])-> QuerySet:
        """Метод возращает список записей модели контент ,которые являются частью рекомендаций клиента"""
        return (self.get_queryset().select_related('content_statistic')
                .filter(slug__in=list_slug)
                .only('title','preview_image','slug','content_statistic__number_of_views'))

    @staticmethod
    def _get_recommendations(instance: Content)-> Dict[str, List[str]]:
        """
        Получает рекомендации для указанного объекта контента.

        Args:
            instance: Объект контента, для которого запрашиваются рекомендации.

        Returns:
            Dict: Словарь рекомендаций.

        Raises:
            ApiClientException: Если произошла ошибка при запросе к серверу рекомендаций.
        """
        try:
            # Готовим данные к отправке
            instance_data = RecommendationDTO.create(instance).to_dict()
            # Делаем запрос на сервер рекомендаций
            response = ContentBasedRecommendationsClient('more_like_this', instance_data).post()
            return response
        except ApiClientException as e:
            raise

    def get_queryset(self) -> QuerySet[Content]:
        # Получаем статус подписки пользователя
        status_subscription = user_status_subscription(self.request.user)

        # Если у пользователя есть активная подписка, возвращаем все контенты
        if status_subscription:
            return Content.objects.all()

        # Если у пользователя нет активной подписки, возвращаем только бесплатный контент
        return Content.objects.free()

    @staticmethod
    def _extract_list_from_dict(data: Dict[str, List[str]]) -> List[str]:
        """
        Извлекает список строк из словаря по ключу 'slug'.

        Этот метод ожидает, что входные данные будут словарем, где ключ — строка,
        а значение — список строк. Метод извлекает список по ключу 'slug' и выполняет
        проверки на корректность данных.

        Args:
            data (Dict[str, List[str]]): Словарь, содержащий список строк по ключу 'slug'.

        Returns:
            List[str]: Список строк, извлеченный по ключу 'slug'.

        Raises:
            ApiClientException: Если список пустой или данные некорректны.
                - Код ошибки "EMPTY_RESPONSE": если список пустой.
                - Код ошибки "INVALID_DATA_FORMAT": если данные не соответствуют ожидаемому формату.
        """
        list_slug = data.get('slug', [])

        match list_slug:
            case []:
                raise ApiClientException(
                    message='Сервис рекомендаций вернул пустой список. Нет данных для обработки.',
                    error_code="EMPTY_RESPONSE",
                )
            case list() if all(isinstance(slug, str) for slug in list_slug):
                return list_slug
            case _:
                raise ApiClientException(
                    message='Сервис рекомендаций вернул некорректные данные. Ожидался список строк.',
                    error_code="INVALID_DATA_FORMAT",
                )
