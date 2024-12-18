from datetime import datetime, timedelta, timezone
from uuid import uuid4

from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APIClient

from task_scheduler.webhook_timer.models import WebhookTimer


class WebhookTimerViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.set_timer_url = reverse("set_timer")

        self.valid_payload = {
            "hours": 1,
            "minutes": 30,
            "seconds": 15,
            "url": "https://example.com/webhook",
        }

    @freeze_time("2025-01-01 00:00:00")
    def test_set_timer_success(self):
        """Test setting a timer with valid input."""
        payload = {
            "hours": 1,
            "minutes": 30,
            "seconds": 15,
            "url": "https://example.com/webhook",
        }
        expected_expires_at = datetime.now(timezone.utc) + timedelta(
            hours=1, minutes=30, seconds=15
        )

        response = self.client.post(self.set_timer_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert data returned in the response object
        response_data = response.json()
        self.assertTrue(response_data["success"])
        self.assertEqual(response_data["message"], "Timer is created")
        self.assertIn("timer_id", response_data["data"])
        self.assertIn("seconds_left", response_data["data"])
        self.assertEqual(response_data["data"]["seconds_left"], 5415)

        timer_id = response_data["data"]["timer_id"]
        self.assertTrue(WebhookTimer.objects.filter(id=timer_id).exists())

        # Assert the created timer has the correct data
        webhook_timer = WebhookTimer.objects.get(id=timer_id)
        self.assertEqual(webhook_timer.url, payload["url"])
        self.assertEqual(webhook_timer.expires_at, expected_expires_at)
        self.assertFalse(webhook_timer.is_url_called)

    def test_set_timer_validation_error(self):
        """Test setting a timer with invalid input."""
        invalid_payload = {"hours": -1, "minutes": -30, "seconds": -5, "url": "invalid-url"}

        response = self.client.post(self.set_timer_url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["message"], "Validation error")

        error_object = response_data["error"]
        self.assertIsInstance(error_object, dict)
        self.assertIn("hours", error_object)
        self.assertIn("minutes", error_object)
        self.assertIn("seconds", error_object)
        self.assertIn("url", error_object)

    def test_set_timer_zero_duration(self):
        """Test setting a timer with zero total duration."""
        zero_duration_payload = {
            "hours": 0,
            "minutes": 0,
            "seconds": 0,
            "url": "https://example.com/webhook",
        }
        response = self.client.post(self.set_timer_url, zero_duration_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertIn("Validation error", response_data["message"])

        error_object = response_data["error"]
        self.assertIsInstance(error_object, dict)
        self.assertIn("non_field_errors", error_object)
        self.assertEqual(
            "Timer duration must be greater than 0 seconds.", error_object["non_field_errors"][0]
        )

    def test_get_timer_success(self):
        """Test retrieving a timer's remaining time."""
        current_datetime = datetime.now(timezone.utc)

        # Freeze time at the current time
        with freeze_time(current_datetime) as frozen_datetime:
            timer_id = uuid4()
            expires_at = current_datetime + timedelta(seconds=120)
            WebhookTimer.objects.create(
                id=timer_id, url="https://example.com/webhook", expires_at=expires_at
            )

            # Play timer for 10 seconds and assert the response
            frozen_datetime.tick(delta=timedelta(seconds=10))

            response = self.client.get(reverse("get_timer", args=[timer_id]))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response_data = response.json()
            self.assertTrue(response_data["success"])
            self.assertEqual("Timer is found", response_data["message"])
            self.assertIn("seconds_left", response_data["data"])
            self.assertEqual(response_data["data"]["seconds_left"], 110)

            # Play timer a little more than the rest of the time left and assert the response
            frozen_datetime.tick(delta=timedelta(seconds=130))

            response = self.client.get(reverse("get_timer", args=[timer_id]))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response_data = response.json()
            self.assertTrue(response_data["success"])
            self.assertEqual("Timer is found", response_data["message"])
            self.assertIn("seconds_left", response_data["data"])
            self.assertEqual(response_data["data"]["seconds_left"], 0)

    def test_get_timer_not_found(self):
        """Test retrieving a timer that does not exist."""
        response = self.client.get(reverse("get_timer", args=[uuid4()]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual("Timer not found", response_data["message"])
        self.assertIn("No timer matches the given id", response_data["error"])

    def test_get_timer_invalid_id(self):
        """Test retrieving a timer with an invalid UUID."""
        response = self.client.get(reverse("get_timer", args=["invalid-uuid"]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual("Validation error", response_data["message"])
        self.assertIn("The timer_id must be UUID", response_data["error"])
