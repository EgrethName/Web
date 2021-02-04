from django import forms
from .models import Answer
from .models import Question


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def clean_text(self):
        text = self.cleaned_data['text']
        return text

    def save(self):
        ask = Question(**self.cleaned_data)
        ask.save()
        return ask


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, question=None, *args, **kwargs):
        self.question = question
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean_text(self):
        text = self.cleaned_data['text']
        return text

    def save(self):
        self.cleaned_data['question_id'] = self.question.id
        ask = Answer(**self.cleaned_data)
        ask.save()
        return ask

