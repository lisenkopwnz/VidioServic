from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from content.filters import ContentFilter
from content.models.model_content import Content
from content.paginators import ContentPaginator
from content.serializers import ContentSerializer
from content.services import user_status_subscription


class ContentViewSet(ModelViewSet):

    """API реализует методы create, list, retrieve, update, destroy
        экземпляра модели Content"""

    serializer_class = ContentSerializer
    pagination_class = ContentPaginator
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ContentFilter
    search_fields = ['title', 'description']
    lookup_field = 'slug'

    # а данный момент операции получения с помошью фильтров
    # списка обЪектов ,а также одной записи
    def get_queryset(self):
        # Получаем статус подписки пользователя
        status_subscription = user_status_subscription(self.request.user)

        # В соответствии с резултатом возвращаем либо полный набор записей ,либо ограниченный.
        if status_subscription:
            return Content.objects.all()
        return Content.objects.free()
