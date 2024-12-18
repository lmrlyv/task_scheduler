from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import uuid4

from celery.exceptions import Retry
from django.test import TestCase

from task_scheduler.webhook_timer.models import WebhookTimer
from task_scheduler.webhook_timer.tasks import start_timer


class CeleryTaskStartTimerTests(TestCase):

    @patch("task_scheduler.webhook_timer.tasks.requests.post")
    @patch("celery.app.task.Context")
    def test_start_timer_success(
        self, mock_celery_context: MagicMock, mock_requests_post: MagicMock
    ):
        """Test start_timer task successfully triggers webhook and updates db."""
        timer_id = uuid4()
        webhook_url = "https://example.com/webhook"
        expected_payload_to_url = {"id": timer_id}

        # Mock the request.id property of the celery task object
        mock_celery_request = MagicMock()
        mock_celery_request.id = timer_id
        mock_celery_context.return_value = mock_celery_request

        # Mock the requests.post method to return ok response
        mock_http_response = MagicMock()
        mock_http_response.ok = True
        mock_requests_post.return_value = mock_http_response

        WebhookTimer.objects.create(id=timer_id, url=webhook_url, expires_at=datetime.now())

        start_timer()

        # Assert the payload sent to webhook url
        self.assertEqual(mock_requests_post.call_count, 1)
        mock_requests_post.assert_called_with(webhook_url, json=expected_payload_to_url)

        # Assert if the task entry in the database gets updated after executing start_timer task
        webhook_timer = WebhookTimer.objects.get(id=timer_id)
        self.assertTrue(webhook_timer.is_url_called)

    @patch("task_scheduler.webhook_timer.tasks.start_timer.retry")
    @patch("task_scheduler.webhook_timer.tasks.requests.post")
    @patch("celery.app.task.Context")
    def test_start_timer_retry(
        self,
        mock_celery_context: MagicMock,
        mock_requests_post: MagicMock,
        mock_start_timer_retry: MagicMock,
    ):
        """Test start_timer task retries if triggering webhook fails."""
        timer_id = uuid4()

        # Mock the request.id property of the celery task object
        mock_celery_request = MagicMock()
        mock_celery_request.id = timer_id
        mock_celery_context.return_value = mock_celery_request

        # Mock the requests.post method to retrun not ok response
        mock_http_response = MagicMock()
        mock_http_response.ok = False
        mock_requests_post.return_value = mock_http_response

        # Mock the retry method of task to raise Retry exception when called
        mock_start_timer_retry.side_effect = Retry()

        WebhookTimer.objects.create(
            id=timer_id, url="https://example.com/webhook", expires_at=datetime.now()
        )

        # Assert if the task gets retried after triggering webhook fails
        with self.assertRaises(Retry):
            start_timer()

    @patch("task_scheduler.webhook_timer.tasks.__trigger_webhook")
    @patch("celery.app.task.Context")
    def test_start_timer_no_db_entry(
        self, mock_celery_context: MagicMock, mock_trigger_webhook: MagicMock
    ):
        """Test start_timer task stops proceeding if there is no db entry found."""
        timer_id = uuid4()

        # Mock the request.id property of the celery task object
        mock_celery_request = MagicMock()
        mock_celery_request.id = timer_id
        mock_celery_context.return_value = mock_celery_request

        # With no entry in the database, test if the trigger_webhook function gets called
        start_timer()
        self.assertEqual(mock_trigger_webhook.call_count, 0)
