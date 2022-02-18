from django.shortcuts import render
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Post, UserPostRelations
from .serializers import RegisterSerializer, LoginSerializer, PostsSerializer, UserPostRelationSerializer


class RegisterUserApiView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginUserApiView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
