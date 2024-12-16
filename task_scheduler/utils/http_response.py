from django.http import JsonResponse


class JsonResponseSuccess(JsonResponse):

    def __init__(self, message, data, *args, **kwargs):
        data = {"success": True, "message": message, "data": data}
        super().init(data, *args, **kwargs)


class JsonResponseError(JsonResponse):

    def __init__(self, message, data, *args, **kwargs):
        data = {"success": False, "message": message, "error": data}
        super().init(data, *args, **kwargs)
