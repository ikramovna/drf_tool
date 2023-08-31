from django.db.models import Model, CharField, TextField, ForeignKey, PositiveIntegerField, CASCADE, BooleanField

from apps.shared.drf.models import BaseModel


class Quiz(BaseModel):
    title = CharField(max_length=100)
    description = TextField()

    def __str__(self):
        return self.title


class Question(BaseModel):
    quiz = ForeignKey(Quiz, CASCADE)
    text = TextField()
    time_limit = PositiveIntegerField(default=30)  # Time limit in seconds

    def __str__(self):
        return self.text


class Choice(BaseModel):
    question = ForeignKey(Question, CASCADE)
    text = CharField(max_length=200)
    is_correct = BooleanField(default=False)

    def __str__(self):
        return self.text


class UserResponse(BaseModel):
    user = ForeignKey('auth.User', CASCADE)
    question = ForeignKey(Question, CASCADE)
    selected_choice = ForeignKey(Choice, CASCADE)
    response_time = PositiveIntegerField()  # Time taken to answer in seconds

    def __str__(self):
        return f"{self.user} - {self.question}"
