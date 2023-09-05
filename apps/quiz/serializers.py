from django.contrib.auth.models import User
from django.core import serializers
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from .models import Quiz, Question, Choice, UserResponse


class QuizSerializer(ModelSerializer):
    # questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description')


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'text', 'is_correct')


class QuestionSerializer(ModelSerializer):
    choices = SerializerMethodField()

    def get_choices(self, obj):
        choices = Choice.objects.filter(question=obj)
        return ChoiceSerializer(choices, many=True).data

    class Meta:
        model = Question
        fields = ('id', 'text', 'choices')


class UserResponseSerializer(ModelSerializer):
    question_id = serializers.CharField(max_length=255, write_only=True)
    choice_id = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = UserResponse
        fields = ('question_id', 'choice_id')

    def validate(self, attrs):
        attrs['quize'] = Question.objects.filter(id=attrs.get('question_id')).first().quiz
        attrs['user'] = User.objects.filter(id=self.initial_data['user']).first()
        if Choice.objects.filter(id=attrs.get('choice_id')).first().is_correct:
            attrs["answer"] = 1
        else:
            attrs["answer"] = 0
        attrs.pop('question_id')
        attrs.pop('choice_id')
        return super().validate(attrs)

    def create(self, validated_data):
        obj = UserResponse.objects.filter(user=validated_data['user'], quize=validated_data['quize']).first()
        if obj:
            obj.answer += validated_data['answer']
            obj.save()
            return obj
        return super().create(validated_data)


class UserListSerializer(Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    answer_user = serializers.SerializerMethodField()

    def get_answer_user(self, obj):
        return f"{obj['answer_user']}"
