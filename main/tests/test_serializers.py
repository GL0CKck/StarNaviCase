from starnavi.starnavicase.main.models import User, Post, UserPostRelations

from django.test import TestCase


class PostSerializer(TestCase):

    def test_reg(self):
        user1 = User.objects.create_user(email='hogo@ua.com', username='Hugovagi', password='12345')
        user2 = User.objects.create_user(email='hogo1@ua.com', username='Hugovagi1', password='12345')

        post1 = Post.objects.create(title='Djangotest', text_post='testcasedjango', owner_post=user1)
        post2 = Post.objects.create(title='Djangotest', text_post='testcasedjango', owner_post=user2)

        UserPostRelations.objects.create(user=user2, posts=post1, like=True)
        UserPostRelations.objects.create(user=user1, posts=post2, dislike=True)
