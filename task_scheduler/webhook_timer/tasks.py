import requests
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from celery.utils.log import get_task_logger
from django.db import transaction

from task_scheduler.webhook_timer.models import WebhookTimer
from task_scheduler.webhook_timer.utils.exceptions import WebhookTriggerError


logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    acks_late=True,
    task_reject_on_worker_lost=True,
    max_retries=3,
    default_retry_delay=10,
)
def start_timer(self):
    """Celery task to trigger a webhook when the timer expires.

    This task must be enqueued by setting either eta (estimated time of arrival) or countdown
    parameters to ensure delay in execution.

    Args:
        self (Task): The current Celery task instance.

    Configuration:
        - acks_late: Ensures the task is acknowledged only after successful execution, enabling
          retries in case of worker failure.
        - task_reject_on_worker_lost: Rejects the task if the worker processing it is lost.
        - max_retries: Limits the number of retries for the task to 3.
        - default_retry_delay: Sets the delay between retries to 10 seconds.

    Raises:
        MaxRetriesExceededError: If the maximum number of retries is exceeded.
        Exception: Reraises any exception encountered during processing for retry.

    Side Effects:
        Sets the 'is_url_called' field of the associated WebhookTimer object to True in the
        database if webhook is successfully triggered.
    """
    timer_id = start_timer.request.id
    try:
        webhook_timer = WebhookTimer.objects.get(id=timer_id)

        url = webhook_timer.url

        if webhook_timer.is_url_called:
            logger.warning(
                f"Webhook has already been fired to '{url}'. Task '{timer_id}' cancelled"
            )
            return

        __trigger_webhook(url)
        __mark_webhook_triggered_in_db(webhook_timer)

    except WebhookTimer.DoesNotExist:
        logger.error(f"WebhookTimer {timer_id} does not exist.")
    except Exception as err:
        logger.error(f"Error updating WebhookTimer '{timer_id}': {str(err)}")
        try:
            raise self.retry(exc=err)
        except MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for timer_id: {timer_id}")


def __trigger_webhook(url: str):
    logger.debug(f"Firing webhook to url '{url}'")
    response = requests.post(url)

    if response.ok:
        logger.info(f"Successfully fired a webhook to '{url}'")
    else:
        err_message = f"Failed to fire a webhook to '{url}', status code: {response.status_code}"
        logger.error(err_message)

        # Retries the task
        raise WebhookTriggerError(err_message)


def __mark_webhook_triggered_in_db(webhook_timer: WebhookTimer):
    with transaction.atomic():
        webhook_timer.is_url_called = True
        webhook_timer.save()
