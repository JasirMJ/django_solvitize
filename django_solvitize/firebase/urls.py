from django.urls import path
from .views import (FirebaseUserLookupView, SendNotificationView, SendTopicNotificationView, 
                    SubscribeTopicView, UnsubscribeTopicView)

urlpatterns = [
    path("auth/lookup/", FirebaseUserLookupView.as_view(), name="user_lookup"),
    path("notification-token/", SendNotificationView.as_view(), name=""),
    path("notification-topic/", SendTopicNotificationView.as_view(), name=""),
    path("subscribe-topic/", SubscribeTopicView.as_view(), name=""),
    path("unsubscribe-topic/", UnsubscribeTopicView.as_view(), name="")
]
