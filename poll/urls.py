from django.contrib import admin
from django.urls import path

from .views_admin import PollListView as AdminPollListView, PollUpdateOrderingView, PollCreateView,\
    PollUpdateView, PollDestroyView, \
    PollQuestionCreateView, PollQuestionUpdateView, PollQuestionDestroyView
from .views_client import PollListView

urlpatterns = [
    # Admin
    path('list/', AdminPollListView.as_view(), name='fetch-poll-list'),
    path('<int:pk>/update/', PollUpdateView.as_view(), name='update-poll'),
    path('<int:pk>/update/ordering/', PollUpdateOrderingView.as_view(), name='update-poll-ordering'),
    path('<int:pk>/delete/', PollDestroyView.as_view(), name='destroy-poll'),
    path('create/', PollCreateView.as_view(), name='create-poll'),
    path('<int:poll_pk>/question/<int:pk>/update/', PollQuestionUpdateView.as_view(), name='update-poll-question'),
    path('<int:poll_pk>/question/<int:pk>/delete/', PollQuestionDestroyView.as_view(), name='destroy-poll-question'),
    path('<int:poll_pk>/question/add/', PollQuestionCreateView.as_view(), name='create-poll-question'),
    # Simple user (Client)
    path('', PollListView.as_view(), name='client-fetch-poll-list'),
]
