import pytest
from model_mommy import mommy

from ..models import Profile, Post, Tag, PostImage, UserFollowing
from model_mommy.recipe import Recipe, foreign_key
from django.contrib.auth.models import User

user_recipe = Recipe(
    User
)

profile_recipe = Recipe(
    Profile,
    user=foreign_key(user_recipe)
)

post_recipe = Recipe(
    Post,
    author=foreign_key(profile_recipe)
)


tag_recipe = Recipe(
    Tag,
)

post_image_recipe = Recipe(
    PostImage,
    post=foreign_key(post_recipe)
)

follower = Recipe(
    UserFollowing,
    user=foreign_key(user_recipe),
    following_user = foreign_key(user_recipe)
)


@pytest.fixture
def user_factory():
    def maker(**kwargs):
        return user_recipe.make(**kwargs)
    return maker


@pytest.fixture
def profile_factory():
    def maker(**kwargs):
        return profile_recipe.make(**kwargs)
    return maker


@pytest.fixture
def post_factory():
    def maker(**kwargs):
        return post_recipe.make(**kwargs)
    return maker


@pytest.fixture
def tag_factory():
    def maker(**kwargs):
        return tag_recipe.make(**kwargs)
        # return mommy.make_recipe(
        #     'tag_recipe', **kwargs
        # )
    return maker


@pytest.fixture
def post_image_factory():
    def maker(**kwargs):
        return post_image_recipe.make(**kwargs)
    return maker


@pytest.fixture
def follower_factory():
    def maker(**kwargs):
        return follower_factory.make(**kwargs)
    return maker
