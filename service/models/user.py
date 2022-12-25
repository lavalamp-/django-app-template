from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class ServiceUser(AbstractUser):
    """This is a custom user class used for the application users."""

    id = models.AutoField(primary_key=True)
    guid = models.UUIDField(default=uuid4, editable=False, db_index=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
