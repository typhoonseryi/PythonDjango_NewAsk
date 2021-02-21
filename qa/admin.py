from django.contrib import admin
from .forms import QuestionAdminForm, AnswerAdminForm, CustomUserChangeForm, CustomUserCreationForm
from .models import Question, Answer, User


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ['id', 'title', 'rating', 'author']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    form = AnswerAdminForm
    list_display = ['author', 'question', 'rating']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'is_staff', 'userpic', 'is_verified']