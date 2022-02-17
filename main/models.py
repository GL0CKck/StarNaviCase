from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Post(models.Model):
    title = models.CharField(max_length=124, verbose_name='Название')
    owner_post = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   related_name='my_posts')
    text_post = models.TextField()
    readers = models.ManyToManyField(User, through='UserPostRelations',
                                     related_name='posts')


class UserPostRelations(models.Model):
    like_or_dislike = ((0, 'Dislike'),
                       (1, 'Like'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)