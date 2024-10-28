from django.urls import path, include
from rest_framework import routers

from content.views import ContentViewSet

app_name = 'content'

router = routers.SimpleRouter()
router.register(r'content', ContentViewSet, basename='content')

urlpatterns = [
    path('', include(router.urls)),
    ]
