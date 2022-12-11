from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import *


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1')


class SearchForm(forms.Form):
    series_name = forms.CharField()

class ScoreForm(forms.Form):
    series_score = forms.IntegerField(min_value=1,
                                      max_value=10,
                                      step_size=1,
                                      widget=forms.NumberInput,
                                      label="Ваша оценка",
                                      required=False)


