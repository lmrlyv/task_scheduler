from django.http import JsonResponse


class JsonResponseSuccess(JsonResponse):
    """
    Custom response class for successful requests.

    This class is used to return a JSON response indicating a successful operation.
    The response includes a success flag, a message, and any associated data.

    Attributes:
        message (str): A message describing the success of the operation.
        data (dict): The data associated with the success (optional).

    Example Usage:
        JsonResponseSuccess("Operation successful", {"key": "value"})
    """

    def __init__(self, message, data, *args, **kwargs):
        data = {"success": True, "message": message, "data": data}
        super().__init__(data, *args, **kwargs)


class JsonResponseError(JsonResponse):
    """
    Custom response class for error responses.

    This class is used to return a JSON response indicating an error.
    The response includes a failure flag, an error message, and any additional error data.

    Attributes:
        message (str): A message describing the error that occurred.
        data (dict): The error details, such as validation issues or specific error information.

    Example Usage:
        JsonResponseError("Validation failed", {"field": "email"})
    """

    def __init__(self, message, data, *args, **kwargs):
        data = {"success": False, "message": message, "error": data}
        super().__init__(data, *args, **kwargs)
