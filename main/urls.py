from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)
from rest_framework.routers import DefaultRouter

from .views import LoginUserApiView, RegisterUserApiView, PostCreateViewSet, PostLikeOrDislikeUser

app_name = 'main'
router = DefaultRouter()
router.register('post', PostCreateViewSet)
router.register('post_relation', PostLikeOrDislikeUser)

urlpatterns = [
    path('register/', RegisterUserApiView.as_view(), name='create_user'),
    path('login/', LoginUserApiView.as_view(), name='login_user'),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]