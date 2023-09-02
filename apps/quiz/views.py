from django.utils import timezone
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Quiz, Question, Choice, UserResponse
from .pagination import CustomPagination
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer, UserResponseSerializer


class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    pagination_class = CustomPagination
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [IsAuthenticatedOrReadOnly]


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = CustomPagination
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def start_timer(self, request, pk=None):
        question = self.get_object()
        question.start_time = timezone.now()
        question.save()
        return Response({'message': 'Timer started.'})

    def get_remaining_time(self, request, pk=None):
        question = self.get_object()
        if not question.start_time:
            return Response({'message': 'Timer not started.'}, status=status.HTTP_400_BAD_REQUEST)

        elapsed_time = (timezone.now() - question.start_time).total_seconds()
        remaining_time = question.time_limit - elapsed_time
        return Response({'remaining_time': remaining_time})


class ChoiceListCreateView(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    pagination_class = CustomPagination
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserResponseListCreateView(generics.ListCreateAPIView):
    queryset = UserResponse.objects.all()
    serializer_class = UserResponseSerializer
    pagination_class = CustomPagination
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Check if this is  last question for the user
        user_responses_count = UserResponse.objects.filter(user=request.user).count()
        total_questions = Question.objects.count()

        if user_responses_count == total_questions:
            # Calculate  marks and percentage
            total_marks = UserResponse.objects.filter(user=request.user, question__choice__is_correct=True).count()
            percentage = (total_marks / total_questions) * 100

            return Response({
                'message': 'Quiz completed!',
                'total_marks': total_marks,
                'percentage': percentage,
            })

        return Response({'message': 'Move to the next Quiz'})
