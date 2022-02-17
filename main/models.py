from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.db import models, transaction
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Проверте электронную почту')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password=password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(max_length=30, unique=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self


class Post(models.Model):
    title = models.CharField(max_length=124)
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