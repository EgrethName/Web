from django import forms
from .models import Answer, Question, SiteUser
from django.contrib.auth.hashers import make_password


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, author=None, *args, **kwargs):
        self.author = author
        super(AskForm, self).__init__(*args, **kwargs)

    def save(self):
        self.cleaned_data['author_id'] = self.author.id
        question = Question(**self.cleaned_data)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, author=None, question=None, *args, **kwargs):
        self.author = author
        self.question = question
        super(AnswerForm, self).__init__(*args, **kwargs)

    def save(self):
        self.cleaned_data['question_id'] = self.question.id
        self.cleaned_data['author_id'] = self.author.id
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer


class SignupForm(forms.Form):
    username = forms.CharField(max_length=15)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        password = self.cleaned_data['password']
        hashed_pass = make_password(password, salt='1', hasher='md5')
        return hashed_pass

    def save(self):
        user = SiteUser(**self.cleaned_data)
        user.save()
        return user


class SiteLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
