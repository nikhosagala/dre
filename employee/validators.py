from django import forms


class ValidatorResultAdd(forms.Form):
    period = forms.CharField(max_length=100)


class AnswerValidator(forms.Form):
    value = forms.IntegerField()
