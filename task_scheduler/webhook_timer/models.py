import uuid

from django.db import models


class WebhookTimer(models.Model):
    """Model representing a webhook timer.

    This model is used to store information about a scheduled webhook.

    Attributes:
        id (UUIDField): Unique identifier for the webhook timer or the celery task (primary key).
        expires_at (DateTimeField): The time when the timer expires and the webhook should be
            triggered.
        url (URLField): The URL to which the webhook will be sent when the timer expires.
        is_url_called (BooleanField): A flag indicating whether the webhook has already been
            called.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expires_at = models.DateTimeField()
    url = models.URLField()
    is_url_called = models.BooleanField(default=False)
