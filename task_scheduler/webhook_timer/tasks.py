import requests
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from celery.utils.log import get_task_logger
from django.db import transaction

from task_scheduler.webhook_timer.models import WebhookTimer


logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def start_timer(self, timer_id):
    try:
        logger.info(f"timer_id: '{timer_id}'")
        webhook_timer = WebhookTimer.objects.get(id=timer_id)
        url = webhook_timer.url

        response = requests.get(url)

        if response.ok:
            logger.info(f"Successfully fired a webhook to '{url}'")
        else:
            logger.error(
                f"Failed to fire a webhook to '{url}', status code: {response.status_code}"
            )

        webhook_timer.is_url_called = True
        webhook_timer.save()
        transaction.commit()

    except WebhookTimer.DoesNotExist:
        logger.error(f"WebhookTimer {timer_id} does not exist.")
    except Exception as err:
        logger.error(f"Error updating WebhookTimer '{timer_id}': {str(err)}")
        try:
            raise self.retry(exc=err)
        except MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for timer_id: {timer_id}")
