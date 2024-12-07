from django.urls import path

from . import views

urlpatterns = [
    path('',views.ErrorAppAPI.as_view()),

]