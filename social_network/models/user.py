import uuid
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID",
    )


def update_user_last_request_timestamp(user: User) -> None:
    cache.set(f"user_last_request__{user.id}", timezone.now(), None)


def get_user_last_request_timestamp(user: User) -> Optional[timezone.datetime]:
    return cache.get(f"user_last_request__{user.id}", None)
