from django.http import QueryDict
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Quiz, Question
from .pagination import CustomPagination
from .serializers import QuizSerializer, QuestionSerializer, UserResponseSerializer


class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    pagination_class = CustomPagination
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [IsAuthenticatedOrReadOnly]


class QuestionListView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # pagination_class = CustomPagination
    parser_classes = (FormParser, MultiPartParser)

    lookup_url_kwarg = 'quiz_id'  # Custom lookup field name

    def get_queryset(self):
        quiz_id = self.kwargs.get(self.lookup_url_kwarg)
        if quiz_id:
            return Question.objects.filter(quiz_id=quiz_id)
        else:
            return Question.objects.all()


class UserResponseCreateView(CreateAPIView):
    serializer_class = UserResponseSerializer
    pagination_class = CustomPagination
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        data = QueryDict(f"question_id={request.data.get('question_id')}"
                         f"&choice_id={request.data.get('choice_id')}"
                         f"&user={request.user.pk}")
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


