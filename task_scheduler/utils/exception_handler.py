import logging
import traceback

from rest_framework.views import exception_handler

from task_scheduler.utils.http_response import JsonResponseError


logger = logging.getLogger("task_scheduler")


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        data = str(exc)
        logger.error(traceback.format_exc())
        return JsonResponseError("Unknown error", data, status=500)

    return JsonResponseError("", response.data, response.status_code)
