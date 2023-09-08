from django.db.models import Model, CharField, TextField, ForeignKey, CASCADE, BooleanField, \
    IntegerField

from apps.shared.drf.models import BaseModel


class Quiz(BaseModel):
    title = CharField(max_length=100)
    description = TextField()

    def __str__(self):
        return self.title


class Question(BaseModel):
    quiz = ForeignKey(Quiz, CASCADE)
    question = TextField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.question

    def get_answers(self):
        answers = []
        for i in self.answers.all():
            answers.append(
                {
                    'id': i.id,
                    'answer': i.answer,
                    'is_correct': i.is_correct
                }
            )
        return answers

    def get_correct_answers(self):
        return self.answers.filter(is_correct=True)


class Choice(BaseModel):
    question = ForeignKey('Question', CASCADE, related_name='answers')
    answer = CharField(max_length=200)
    is_correct = BooleanField(default=False)

    def __str__(self):
        return self.answer


class UserResponse(BaseModel):
    user = ForeignKey('auth.User', CASCADE)
    quize = ForeignKey('Quiz', CASCADE)
    answer = IntegerField()

    def __str__(self):
        return f"{self.user} - {self.quize}"
