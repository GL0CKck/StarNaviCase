from rest_framework import serializers

from .models import User, Post, UserPostRelations


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PostReadersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class PostsSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner_post.username', default='', read_only=True)
    annotated_likes = serializers.IntegerField(read_only=True)
    annotated_dislikes = serializers.IntegerField(read_only=True)
    readers = PostReadersSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'text_post', 'readers', 'owner', 'annotated_likes', 'annotated_dislikes')


class UserPostRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPostRelations
        fields = ('', '', '')