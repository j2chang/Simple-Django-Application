from django import forms
from django.forms import HiddenInput
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

ChoiceFormSet = forms.inlineformset_factory(
    Question,
    Choice,
    fields=['choice_text'],
    extra=3,
    can_delete=False,
    widgets={'DELETE': HiddenInput()},
)