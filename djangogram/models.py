import re

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    bio = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(
        blank=True, null=True, default='default.png'
    )

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance,  **kwargs):
    #     instance.profile.save()


class Post(models.Model):
    description = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=True
    )
    image = models.ImageField(blank=True, null=True)

    def render_description_to_html(self):
        from djangogram.utils import extract_tags
        tags = extract_tags(self)
        new_description = self.description
        url = reverse('tag')
        for tag in tags:
            new_description = new_description.replace(f'#{tag[0]}', f'<a href="{url}?tag={tag[0]}">#{tag[0]}</a>')
        return new_description


class PostImage(models.Model):
    post = models.ForeignKey(
        Post, default=None, on_delete=models.CASCADE, related_name='post_image'
    )
    image = models.ImageField(blank=True)


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
