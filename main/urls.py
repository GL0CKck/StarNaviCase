from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)
from rest_framework.routers import DefaultRouter

from .views import RegisterUserApiView, PostCreateViewSet, PostLikeOrDislikeUser, LastLoginApiView

app_name = 'main'
router = DefaultRouter()
router.register('post', PostCreateViewSet)
router.register('post_relation', PostLikeOrDislikeUser)

urlpatterns = [
    path('register/', RegisterUserApiView.as_view(), name='create_user'),
    path('user/login/', LastLoginApiView.as_view(), name='last_login_last_request'),
    path('api/', include(router.urls)),
    path('api/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]