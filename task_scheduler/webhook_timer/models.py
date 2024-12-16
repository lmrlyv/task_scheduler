import uuid

from django.db import models


class WebhookTimer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expires_at = models.DateTimeField()
    url = models.URLField()
    is_url_called = models.BooleanField(default=False)
