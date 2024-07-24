from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SavingsGoal, Contribution
from .models import FinancialData
from .models import UserProfile



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    income = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    expenses = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'income', 'expenses']

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

class FinancialDataForm(forms.ModelForm):
    class Meta:
        model = FinancialData
        fields = ['income', 'expenses', 'savings', 'entertainment', 'dining_out']
        widgets = {
            'income': forms.NumberInput(attrs={'step': '0.01'}),
            'expenses': forms.NumberInput(attrs={'step': '0.01'}),
            'savings': forms.NumberInput(attrs={'step': '0.01'}),
            'entertainment': forms.NumberInput(attrs={'step': '0.01'}),
            'dining_out': forms.NumberInput(attrs={'step': '0.01'}),
        }

class FinancialDataForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['income', 'expenses']

class FinancialDataForm(forms.Form):
    income = forms.DecimalField(label='Monthly Income', max_digits=10, decimal_places=2)
    expenses = forms.DecimalField(label='Monthly Expenses', max_digits=10, decimal_places=2)
    savings = forms.DecimalField(label='Monthly Savings', max_digits=10, decimal_places=2)
