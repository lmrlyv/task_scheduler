from rest_framework.serializers import IntegerField, Serializer, URLField, ValidationError


class SetTimerSerializer(Serializer):
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
