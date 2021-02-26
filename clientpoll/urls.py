from django.contrib import admin
from django.urls import path

from .views import ClientPollCreateView, ClientPollAnswerCreateView

urlpatterns = [
    path('create/', ClientPollCreateView.as_view(), name='create-client-poll'),
    path('answer/submit/', ClientPollAnswerCreateView.as_view(), name='create-client-poll-result'),
]