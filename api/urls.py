from api.spectacular.urls import urlpatterns as doc_api
from accounts.urls import urlpatterns as auth_api
from content.urls import urlpatterns as content_api
from django.urls import path, include
app_name = 'api'


urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]
urlpatterns += doc_api
urlpatterns += auth_api
urlpatterns += content_api
