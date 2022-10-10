from django.conf import settings
from django.db import models


class URL(models.Model):
    original_link = models.URLField(max_length=1000)
    short_url = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    num_visits = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="urls")

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Urls"

    def __str__(self):
        return self.original_link
