from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1')


class SearchForm(forms.Form):
    series_name = forms.CharField()

class UsersInfo(forms.Form):
    def __init__(self, *args, **kwargs):
        self.episodes_amount = kwargs.pop('episodes_amount', None)
        super(UsersInfo, self).__init__(*args, **kwargs)

    series_score = forms.IntegerField(min_value=1,
                                      max_value=10,
                                      step_size=1,
                                      widget=forms.NumberInput,
                                      label="Ваша оценка",
                                      required=False)
    viewed_episodes_amount = forms.IntegerField(min_value=0,
                                                label="Число просмотренных серий",
                                                widget=forms.NumberInput,
                                                required=False)

    def clean_viewed_episodes_amount(self):
        data = self.cleaned_data['viewed_episodes_amount']
        if data == None:
            return data
        if data > self.episodes_amount:
            raise ValidationError(f"You must write number not greater than {self.episodes_amount}")
        return data

