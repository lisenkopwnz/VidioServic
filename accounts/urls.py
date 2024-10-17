from django.urls import path
from accounts.serializers.views import users

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )


urlpatterns = [
    path('users/reg', users.RegistrationView.as_view(), name='reg'),
    path('users/profile', users.ProfileView.as_view(), name='profile'),
    path('users/change-password', users.ChangePasswordView.as_view(), name='change_pass'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
