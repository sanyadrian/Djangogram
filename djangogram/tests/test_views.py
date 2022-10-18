import pytest
from ..models import Profile, User, Post, Tag
from django.urls import reverse
from .test_config import (
    post_factory, profile_factory, user_factory, tag_factory
)
from django.contrib.auth.models import User
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
        description='asdad', author=profile, image='static/images/defaulf.png'
    )
    url = reverse('post', kwargs={'pk': post.id})
    response = client.get(url)
    assert response.status_code == 200


def test_login(client, user_factory):
    credentials = {
        'username': 'admin',
        'password': 'password'
    }
    user = user_factory(
        **credentials
    )
    url = reverse('login')
    response = client.post(url, credentials, follow=True)
    assert response.context['user'] == user
    # assert response.context['url'] == reverse('profiles')
    assert response.status_code == 200



