from datetime import datetime
from django.db.models import Q, Count, Case, When
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Post, UserPostRelations, User
from .serializers import RegisterSerializer, PostsSerializer, UserPostRelationSerializer, \
    UserActivitySerializer, StatisticsLikesSerializer
import json

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


class TotalLikePostApiView(APIView):

    def get(self, request):
        date_format = '%d-%m-%y'
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        date_from = datetime.strptime(date_from, date_format)
        date_to = datetime.strptime(date_to, date_format)

        total_like = UserPostRelations.objects.filter(Q(date_create__gte=date_from) & Q(date_create__lte=date_to))
        total_like = total_like.values().aggregate(total_likes=Count(Case(When(like_or_dislike=1, then=1))))
        total_dislike = UserPostRelations.objects.filter(Q(date_create__gte=date_from) & Q(date_create__lte=date_to))
        total_dislike = total_dislike.values().aggregate(total_dislikes=Count(Case(When(like_or_dislike=0, then=1))))
        response_data = {
            'total_like': total_like,
            'total_dislike': total_dislike
        }
        return Response(response_data)


class StatisticsLikeModelViewSet(ModelViewSet):
    queryset = Post.objects.all().annotate(annotated_like=Count(Case(When(userpostrelations__like_or_dislike=1, then=1)))).order_by('id')
    serializer_class = StatisticsLikesSerializer
    permission_classes = (IsAdminUser, )