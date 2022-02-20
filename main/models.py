from django.contrib.auth.models import (AbstractUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Имя пользователя должно быть указанно')
        if not email:
            raise ValueError('Почта пользователя должна быть указанна')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(self, username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password=password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=55, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_request = models.DateTimeField(blank=True, null=True)

    object = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('fist_name', 'last_name')


class Post(models.Model):
    title = models.CharField(max_length=124)
    owner_post = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   related_name='my_posts')
    text_post = models.TextField()
    readers = models.ManyToManyField(User, through='UserPostRelations',
                                     related_name='posts')


class UserPostRelations(models.Model):
    LIKE_DISLIKE_CHOICES = (
        (0, 'dislike'),
        (1, 'like')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_or_dislike = models.PositiveSmallIntegerField(choices=LIKE_DISLIKE_CHOICES, null=True)