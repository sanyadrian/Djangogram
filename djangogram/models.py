from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    profile_image = models.ImageField(
        blank=True, null=True, default='default.png'
    )


class Post(models.Model):
    description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=True
    )


class Tag(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    posts = models.ManyToManyField(Post, related_name='tags')

    def __str__(self):
        return self.name
    #
    # class Meta:
    #     verbose_name = 'asdrt'


class Photo(models.Model):
    image = models.ImageField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Like(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_likes'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post_likes'
    )
