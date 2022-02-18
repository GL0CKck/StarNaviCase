from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Post, UserPostRelations, User
from .serializers import RegisterSerializer, LoginSerializer, PostsSerializer, UserPostRelationSerializer, \
    UserActivitySerializer


class RegisterUserApiView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostCreateViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    permission_classes = (IsAuthenticated, )
    filter_fields = ('title',)
    ordering_fields = ('title', )

    def perform_create(self, serializer):
        serializer.validated_data['owner_post'] = self.request.user
        serializer.save()


class PostLikeOrDislikeUser(UpdateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = UserPostRelations.objects.all()
    serializer_class = UserPostRelationSerializer
    lookup_field = 'posts'

    def get_object(self):
        obj, _ = UserPostRelations.objects.get_or_create(user=self.request.user, posts_id=self.kwargs['posts'])

        return obj


class LastLoginApiView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser, )
    serializer_class = UserActivitySerializer
