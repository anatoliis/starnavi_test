from django.db import models

from social_network.models.abstract.created_at import AbstractCreatedAtModel


class Post(AbstractCreatedAtModel):
    user = models.ForeignKey("User", related_name="posts", on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        db_table = "posts"
        ordering = ("-created_at",)
        get_latest_by = ("-created_at",)
