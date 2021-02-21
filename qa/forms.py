from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Question, Answer, User


class RequiredFieldsMixin():

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        fields_required = getattr(self.Meta, 'fields_required', None)

        if fields_required:
            for key in self.fields:
                if key not in fields_required:
                    self.fields[key].required = False


class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = {
            'title',
            'text',
            'rating',
            'author'
        }

class AnswerAdminForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = {
            'text',
            'author',
            'question',
            'rating'
        }

class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

    def save(self, id, user):
        self.cleaned_data['author'] = user
        self.cleaned_data['question'] = Question.objects.get(id=id)
        post = Answer(**self.cleaned_data)
        post.save()
        return post


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']


class CustomUserCreationForm(RequiredFieldsMixin, UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['username', 'email', 'first_name', 'second_name', 'userpic']
        fields_required = ['username', 'password']


class CustomUserChangeForm(RequiredFieldsMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'second_name', 'userpic')
        fields_required = []
