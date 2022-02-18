from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import Post, User, UserPostRelations


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if email is None:
            raise serializers.ValidationError('Need email')

        if password is None:
            raise serializers.ValidationError('Need password')

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError('User was not found')
        return {
            'user': user.email
        }

    class Meta:
        model = User
        fields = ('email', 'password')


class PostReadersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class PostsSerializer(serializers.ModelSerializer):
    owner_post = serializers.CharField(source='owner_post.username', default='', read_only=True)
    readers = PostReadersSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'text_post', 'readers', 'owner_post')


class UserPostRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPostRelations
        fields = ('user', 'posts', 'like_or_dislike')