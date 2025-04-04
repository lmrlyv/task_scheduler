# Generated by Django 5.1.4 on 2024-12-16 20:54

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WebhookTimer",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("expires_at", models.DateTimeField()),
                ("url", models.URLField()),
                ("is_url_called", models.BooleanField(default=False)),
            ],
        ),
    ]
