import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from task_scheduler.utils.http_response import JsonResponseError, JsonResponseSuccess
from task_scheduler.webhook_timer.models import WebhookTimer
from task_scheduler.webhook_timer.serializers import SetTimerSerializer
from task_scheduler.webhook_timer.tasks import start_timer


logger = logging.getLogger("webhook_timer")


class WebhookTimerView(APIView):
    def post(self, request: HttpRequest, *args, **kwargs):
        data = request.data
        serializer = SetTimerSerializer(data=data)

        if not serializer.is_valid():
            return JsonResponseError("Validation error", serializer.errors, status=400)

        hours = int(data["hours"])
        minutes = int(data["minutes"])
        seconds = int(data["seconds"])
        url = data["url"]

        expiration_td = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        expires_at = datetime.now(timezone.utc) + expiration_td

        # Start a timer in the background
        task = start_timer.apply_async(args=[timer.id], eta=expires_at)

        # Create a new WebhookTimer object in the database
        timer_id = task.id
        timer = WebhookTimer.objects.create(id=timer_id, url=url, expires_at=expires_at)

        return JsonResponseSuccess(
            "Timer is created",
            {"timer_id": str(timer_id), "seconds_left": expiration_td.total_seconds()},
        )

    def get(self, request, timer_id, *args, **kwargs):
        try:
            timer_id = UUID(timer_id)
        except ValueError as err:
            return JsonResponseError(
                "Validation error", f"The timer_id 'timer' must be UUID", status=400
            )

        webhook_timer = get_object_or_404(WebhookTimer, id=timer_id)

        seconds_left = (webhook_timer.expires_at - datetime.now(timezone.utc)).total_seconds()
        if seconds_left < 0:
            seconds_left = 0

        return JsonResponseSuccess("Timer is found", {"seconds_left": int(seconds_left)})
