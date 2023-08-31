from rest_framework.serializers import ModelSerializer

from .models import Quiz, Question, Choice, UserResponse


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class QuizSerializer(ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = '__all__'


class UserResponseSerializer(ModelSerializer):
    class Meta:
        model = UserResponse
        fields = '__all__'
