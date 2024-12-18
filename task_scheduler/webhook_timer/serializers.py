from rest_framework.serializers import IntegerField, Serializer, URLField, ValidationError


class SetTimerSerializer(Serializer):
    """Input serializer the set_timer endpoint.

    This serializer validates the data required to set a webhook timer, including the
    hours, minutes, seconds, and the URL. It ensures that the time is a positive value,
    the total timer duration is greater than zero, and given url is valid.

    Attributes:
        hours (IntegerField): The number of hours for the timer. Must be a non-negative integer.
        minutes (IntegerField): The number of minutes for the timer. Must be a non-negative integer.
        seconds (IntegerField): The number of seconds for the timer. Must be a non-negative integer.
        url (URLField): The URL to which the webhook will be sent when the timer expires.

    Overloading Methods:
        validate(data): Custom validation to ensure the total timer duration is greater than 0 seconds.
    """

    hours = IntegerField(min_value=0, required=True)
    minutes = IntegerField(min_value=0, required=True)
    seconds = IntegerField(min_value=0, required=True)
    url = URLField(required=True)

    def validate(self, data):
        """
        Custom validation to check the total time is within a reasonable limit.
        """
        total_seconds = data["hours"] * 3600 + data["minutes"] * 60 + data["seconds"]
        if total_seconds == 0:
            raise ValidationError("Timer duration must be greater than 0 seconds.")
        return data
