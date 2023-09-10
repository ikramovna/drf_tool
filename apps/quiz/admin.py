from django.contrib import admin

from apps.quiz.models import Quiz, Question, Choice, UserResponse

class ChoiceAdmin(admin.StackedInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoiceAdmin,)


admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserResponse)



