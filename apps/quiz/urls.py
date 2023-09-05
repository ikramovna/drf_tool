from django.urls import path

from apps.quiz.views import (
    UserResponseCreateView, QuizListView, QuestionListView, UserListAPIView)

urlpatterns = [
    path('quize-list', QuizListView.as_view(), name='quiz-list-create'),
    path('question-list/<int:quiz_id>', QuestionListView.as_view(), name='question-list'),
    path('user-response', UserResponseCreateView.as_view(), name='user-response-create'),
    path('user-list', UserListAPIView.as_view(), name='quiz-statistics'),
]
