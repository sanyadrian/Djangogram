import pytest
from model_mommy import mommy

from ..models import Profile, Post, Tag
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
