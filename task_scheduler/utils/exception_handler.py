import logging
import traceback

from rest_framework.views import exception_handler

from task_scheduler.utils.constants import IS_DEBUG_ON
from task_scheduler.utils.custom_responses import JsonResponseError


logger = logging.getLogger("task_scheduler")


def custom_exception_handler(exc, context):
    """Custom exception handler for Django REST Framework.

    This function handles exceptions raised in the application and customizes the response format.
    It ensures the consistent structure from the endpoints.
    """
    response = exception_handler(exc, context)

    if response is None:
        logger.error(traceback.format_exc())
        error_message = str(exc) if IS_DEBUG_ON else "Please contact the system administrator."
        return JsonResponseError("Unknown error", error_message, status=500)

    message = response.data.get("code", "")
    error_message = response.data["detail"] if "detail" in response.data else response.data
    return JsonResponseError(message, error_message, status=response.status_code)
