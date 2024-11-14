from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins
from rest_framework.generics import ListAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.elasticsearch.document import ContentDocument
from content.filters import ContentFilter
from content.models.model_content import Content
from content.paginators import ContentPaginator
from content.serializers import ContentSerializer
from content.services import user_status_subscription


class ContentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     RetrieveModelMixin,
                     GenericViewSet):

    """API реализует методы create, update, destroy, retrieve
        экземпляра модели Content"""

    serializer_class = ContentSerializer
    lookup_field = 'slug'  #Поиск конкретной записи производим по полю slug

    def get_queryset(self):
        # Получаем статус подписки пользователя
        status_subscription = user_status_subscription(self.request.user)

        # Если пользователь анонимен или не оплатил платную подписку возвращаем ему False
        if status_subscription:
            return Content.objects.all()
        return Content.objects.free()


class ElasticsearchView(ListAPIView):

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ContentFilter
    pagination_class = ContentPaginator


    def get_queryset(self):
        """
        Переопределяем метод для фильтрации данных по полю `is_private`
        на основе статуса подписки пользователя.
        """
        queryset = ContentDocument.search().filter("term",
                                            is_private=user_status_subscription(self.request.user))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
