from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from .views import LoginUserApiView, RegisterUserApiView

app_name = 'main'

urlpatterns = [
    path('register/', RegisterUserApiView.as_view(), name='create_user'),
    path('login/', LoginUserApiView.as_view(), name='login_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]