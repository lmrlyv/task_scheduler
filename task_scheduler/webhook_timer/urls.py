from django.urls import path

from task_scheduler.webhook_timer.views import WebhookTimerView


urlpatterns = [
    path("timer", WebhookTimerView.as_view(), name="set_timer"),
    path("timer/<timer_id>/", WebhookTimerView.as_view(), name="get_timer"),
]
