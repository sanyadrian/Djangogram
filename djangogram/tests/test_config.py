import pytest
from ..models import Profile, User, Post, Tag
from model_mommy.recipe import Recipe, foreign_key

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
    posts=foreign_key(post_recipe)
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
    return maker
