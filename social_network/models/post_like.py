from django.db import models

from social_network.models.abstract.created_at import AbstractCreatedAtModel


class PostLike(AbstractCreatedAtModel):
    user = models.ForeignKey("User", related_name="user", on_delete=models.CASCADE)
    post = models.ForeignKey(
        "social_network.Post", related_name="likes", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "post_likes"
        unique_together = ("user", "post")
        ordering = ("-created_at",)
        get_latest_by = ("-created_at",)
