from django.urls import path

from apps.quiz.views import (
    UserResponseCreateView, QuizListView, QuestionListView, UserListAPIView)

urlpatterns = [
    path('quize-list', QuizListView.as_view(), name='quize'),
    path('question-list/<int:quiz_id>', QuestionListView.as_view(), name='question'),
    path('user-response', UserResponseCreateView.as_view(), name='user-response'),
    path('user-list', UserListAPIView.as_view(), name='user-list'),
]
