import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID

from rest_framework.request import Request
from rest_framework.views import APIView

from task_scheduler.utils.custom_responses import JsonResponseError, JsonResponseSuccess
from task_scheduler.webhook_timer.models import WebhookTimer
from task_scheduler.webhook_timer.serializers import SetTimerSerializer
from task_scheduler.webhook_timer.tasks import start_timer


logger = logging.getLogger("webhook_timer")


class WebhookTimerView(APIView):
    """
    Create a new timer for triggering a webhook.

    POST /timer

    Description:
        This endpoint allows the user to create a new timer that triggers a webhook when it
        expires.

    Request Body:
        hours (int): The number of hours for the timer. Must be a non-negative integer.
        minutes (int): The number of minutes for the timer. Must be a non-negative integer.
        seconds (int): The number of seconds for the timer. Must be a non-negative integer.
        url (str): The webhook URL to be triggered when the timer expires. Must be a valid URL.

        Example:
        {
            "hours": 1,
            "minutes": 30,
            "seconds": 15,
            "url": "https://example.com/webhook"
        }

    Responses:
        201 Created:
            Description: The timer is successfully created, and details about the timer are returned.
            Example:
            {
                "success": true,
                "message": "Timer is created",
                "data": {
                    "timer_id": "a7293427-c147-455e-bf41-ddb36eea4119",
                    "seconds_left": 5415
                }
            }
        400 Bad Request:
            Description: The input data is invalid (e.g., negative duration values or invalid URL).
            Example:
            {
                "success": false,
                "message": "Validation error",
                "details": {
                    "url": ["Enter a valid URL."],
                    "hours": ["Ensure this value is greater than or equal to 0."]
                }
            }
    """

    def post(self, request: Request, *args, **kwargs):
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

        # Start the timer in the background
        task = start_timer.apply_async(eta=expires_at)

        # Create a new WebhookTimer object in the database
        timer_id = task.id
        WebhookTimer.objects.create(id=timer_id, url=url, expires_at=expires_at)

        return JsonResponseSuccess(
            "Timer is created",
            {"timer_id": str(timer_id), "seconds_left": expiration_td.total_seconds()},
            status=201,
        )

    def get(self, request: Request, timer_id: str, *args, **kwargs):
        """Retrieve the remaining time for a specific timer.

        GET /timer/<timer_id>/

        Description:
            This endpoint retrieves the remaining time (in seconds) for a timer identified by
            its UUID. If the timer has expired, the remaining time will be returned as `0`.

        Parameters:
            timer_id (str): The UUID of the timer. Must be a valid UUID string.

        Responses:
            200 OK:
                Description: The timer is found, and the remaining time is returned.
                Example:
                {
                    "success": true,
                    "message": "Timer is found",
                    "data": {
                        "seconds_left": 120
                    }
                }
            400 Bad Request:
                Description: The timer_id is invalid (not a UUID).
                Example:
                {
                    "success": false,
                    "message": "Validation error",
                    "details": "The timer_id must be UUID, but given 'invalid-uuid'"
                }
            404 Not Found:
                Description: No timer with the specified ID exists in the database.
                Example:
                {
                    "success": false,
                    "message": "Timer not found",
                    "details": "No timer matches the given id"
                }
        """
        try:
            timer_id = UUID(timer_id)
            webhook_timer = WebhookTimer.objects.get(id=timer_id)
        except ValueError:
            return JsonResponseError(
                "Validation error", f"The timer_id must be UUID, but given '{timer_id}'", status=400
            )
        except WebhookTimer.DoesNotExist:
            return JsonResponseError("Timer not found", "No timer matches the given id", status=404)

        # The expired_at datetime object is in UTC
        seconds_left = (webhook_timer.expires_at - datetime.now(timezone.utc)).total_seconds()
        if seconds_left < 0:
            seconds_left = 0

        return JsonResponseSuccess("Timer is found", {"seconds_left": int(seconds_left)})
