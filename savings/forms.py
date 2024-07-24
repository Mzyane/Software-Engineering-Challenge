from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SavingsGoal, Contribution


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['name', 'target_amount', 'target_date']


class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['goal', 'amount']
        widgets = {
            'goal': forms.Select(),
            'amount': forms.NumberInput(attrs={'type': 'number'}),
        }
