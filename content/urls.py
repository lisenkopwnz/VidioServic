from django.urls import path, include
from rest_framework import routers

from content.views import ContentViewSet, ElasticsearchViewSet

app_name = 'content'

router = routers.SimpleRouter()
router.register(r'content', ContentViewSet, basename='content')
router.register(r'search', ElasticsearchViewSet, basename='search')

urlpatterns = [
    path('', include(router.urls)),
    ]
