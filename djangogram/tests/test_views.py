import pytest
from ..models import Profile, User, Post, Tag
from django.urls import reverse
from .test_config import (
    post_factory, profile_factory, user_factory, tag_factory
)
pytestmark = [pytest.mark.django_db]


def test_views_profile(client, user_factory, profile_factory):
    user = user_factory()
    profile = profile_factory(
        bio='asda', user=user
    )
    url = reverse('profile', kwargs={'pk': profile.id})
    response = client.get(url)
    assert response.status_code == 200


def test_views_post(client, user_factory, profile_factory, post_factory):
    user = user_factory()
    profile = profile_factory(
        bio='asda', user=user
    )
    post = post_factory(
        description='asdad', author=profile
    )
    url = reverse('post', kwargs={'pk': post.id})
    response = client.get(url)
    assert response.status_code == 200


def test_tag(client, post_factory, tag_factory):
    post = Post.objects.create(
        description='asdad'
    )
    tag = Tag.objects.create(
        name='asdaq'
    )
    post.tags.add(tag)
    url = reverse('tag', kwargs={'pk': tag.id})
    response = client.get(url)
    assert response.status_code == 200



