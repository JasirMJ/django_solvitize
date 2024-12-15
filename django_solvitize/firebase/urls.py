from django.urls import path
from .views import FirebaseUserLookupView

urlpatterns = [
    path("auth/lookup/", FirebaseUserLookupView.as_view(), name="user_lookup"),
]
