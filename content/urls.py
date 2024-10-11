from django.urls import path

from content.views import ContentApiView

app_name = 'content'

urlpatterns = [
    path('api/content/', ContentApiView.as_view(), name='content_list')
]
