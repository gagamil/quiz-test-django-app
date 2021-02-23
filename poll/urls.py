from django.contrib import admin
from django.urls import path

from .views_admin import PollCreateView, PollUpdateView, PollDestroyView, \
    PollQuestionCreateView

urlpatterns = [
    path('<int:pk>/update/', PollUpdateView.as_view(), name='update-poll'),
    path('<int:pk>/delete/', PollDestroyView.as_view(), name='destroy-poll'),
    path('create/', PollCreateView.as_view(), name='create-poll'),
    path('<int:poll_pk>/question/add/', PollQuestionCreateView.as_view(), name='create-poll-question'),
    # path('<int:pk>/comment/', ProjectCommentCreateAPIView.as_view(), name='projects-comment-create'),
    # path('<int:pk>/', ProjectsDetailView.as_view(), name='projects-detail'),
    # path('<int:pk>/update/', ProjectsUpdateView.as_view(), name='projects-update'),
    # path('create/', ProjectsCreateView.as_view(), name='projects-create')
]
