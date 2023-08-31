from django.urls import path

from apps.quiz.views import QuizListCreateView, QuestionListCreateView, ChoiceListCreateView, UserResponseListCreateView

urlpatterns = [
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('choices/', ChoiceListCreateView.as_view(), name='choice-list-create'),
    path('user-responses/', UserResponseListCreateView.as_view(), name='user-response-list-create'),
]
