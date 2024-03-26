from uuid import uuid4

import pytest
from faker import Faker
from rest_framework.authtoken.models import Token

from mygreatproject.models import User

USER_1_ID = 1
f = Faker()


@pytest.fixture
def new_user() -> User:
    """Create and return a new user for use in testing."""
    new_user = User(
        email=f"{uuid4()}@sample.com",
        username=f.user_name(),
    )
    new_user.save()
    return new_user


@pytest.fixture
def new_user_api_key(new_user: User) -> str:
    """Test fixture for providing the API key for a new user."""
    token, _ = Token.objects.get_or_create(user=new_user)
    return token.key


@pytest.fixture
def user_1() -> User:
    """Test fixture for providing the user associated with USER_1_ID."""
    try:
        return User.objects.get(id=USER_1_ID)
    except User.DoesNotExist:
        new_user = User(
            email="user1@sample.com",
        )
        new_user.save()
        return new_user


@pytest.fixture
def user_1_api_key(user_1: User) -> str:
    """Test fixture for providing the API key for user_1."""
    token, _ = Token.objects.get_or_create(user=user_1)
    return token.key
