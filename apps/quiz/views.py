from django.http import QueryDict
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Quiz, Question, UserResponse
from .pagination import CustomPagination
from .serializers import QuizSerializer, QuestionSerializer, UserResponseSerializer, UserListSerializer


class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [IsAuthenticatedOrReadOnly]


class QuestionListView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = CustomPagination
    parser_classes = (FormParser, MultiPartParser)

    lookup_url_kwarg = 'quiz_id'

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


class UserListAPIView(APIView):
    def get(self, request):
        user = request.user
        user_responses = UserResponse.objects.filter(user=user)
        quiz_ids = user_responses.values_list('quize_id', flat=True)
        quiz_data = Quiz.objects.filter(id__in=quiz_ids)

        response_data = []

        for quiz in quiz_data:
            user_responses_for_quiz = user_responses.filter(quize=quiz)
            answer_user = f"{user_responses_for_quiz.count()} %"
            response_data.append({
                'id': quiz.id,
                'title': quiz.title,
                'answer_user': answer_user,
            })

        serializer = UserListSerializer(response_data, many=True)
        return Response(serializer.data)
