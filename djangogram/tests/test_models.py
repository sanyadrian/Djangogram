import pytest
from djangogram.models import Profile, User, Post, Tag
from datetime import datetime
from .test_config import (
    user_factory, profile_factory, post_factory, tag_factory,
    post_image_factory
)

@pytest.mark.django_db
def test_profile(user_factory, profile_factory):
    user = user_factory()
    profile = profile_factory(
        bio='asda', user=user
    )
    assert profile.bio == 'asda'
    # assert user.username == user
    assert profile.user == user


@pytest.mark.django_db
def test_post(profile_factory, post_factory):
    profile = profile_factory()
    post = post_factory(
        description='asdad',
        author=profile
    )
    assert post.description == 'asdad'
    assert post.id == 1
    assert post.author == profile


@pytest.mark.django_db
def test_tag(post_factory, tag_factory):
    post = post_factory()
    tag = tag_factory(
        name='asdaq'
    )
    post.tags.add(tag)
    assert tag in post.tags.all()



