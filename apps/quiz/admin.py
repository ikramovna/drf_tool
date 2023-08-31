from django.contrib import admin

from apps.quiz.models import Quiz, Question, Choice, UserResponse

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserResponse)