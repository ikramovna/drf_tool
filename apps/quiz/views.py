from rest_framework import generics, status
from rest_framework.response import Response

from .models import Quiz, Question, Choice, UserResponse
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer, UserResponseSerializer


class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceListCreateView(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class UserResponseListCreateView(generics.ListCreateAPIView):
    queryset = UserResponse.objects.all()
    serializer_class = UserResponseSerializer

    def create(self, request, *args, **kwargs):
        user = request.user  # authentication is required
        question_id = request.data.get('question')
        selected_choice_id = request.data.get('selected_choice')
        response_time = request.data.get('response_time')

        try:
            question = Question.objects.get(pk=question_id)
            selected_choice = Choice.objects.get(pk=selected_choice_id)
        except (Question.DoesNotExist, Choice.DoesNotExist):
            return Response({'detail': 'Question or Choice does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        user_response = UserResponse(user=user, question=question, selected_choice=selected_choice,
                                     response_time=response_time)
        user_response.save()

        is_correct = selected_choice.is_correct
        response_data = {'message': 'Response recorded.', 'is_correct': is_correct}
        return Response(response_data, status=status.HTTP_201_CREATED)
