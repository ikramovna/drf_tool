from django.urls import path

from apps.quiz.views import (
    UserResponseCreateView, QuizListView, QuestionListView)

urlpatterns = [
    path('quize_list', QuizListView.as_view(), name='quiz-list-create'),
    path('question_list/<int:quiz_id>', QuestionListView.as_view(), name='question-list'),
    path('user-response', UserResponseCreateView.as_view(), name='user-response-create'),

]
