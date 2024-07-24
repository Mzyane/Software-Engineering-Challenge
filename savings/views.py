from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, SavingsGoalForm, ContributionForm
from .models import SavingsGoal, Contribution
from django.contrib.auth.forms import AuthenticationForm
from .models import Contribution, SavingsGoal
import datetime
from django.conf import settings
from .forms import FinancialDataForm
from .models import FinancialData
from .analyzer import SavingsBehaviorAnalyzer
from .models import UserProfile
from .forms import FinancialDataForm


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile.objects.get(user=user)
            profile.income = form.cleaned_data['income']
            profile.expenses = form.cleaned_data['expenses']
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session['show_modal'] = True
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    show_modal = request.session.pop('show_modal', False)
    return render(request, 'login.html', {'form': form, 'show_modal': show_modal})


@login_required
def create_goal(request):
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('progress')
    else:
        form = SavingsGoalForm()
    return render(request, 'create_goal.html', {'form': form})


@login_required
def contribute(request):
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            goal = form.cleaned_data['goal']
            amount = form.cleaned_data['amount']

            try:
                goal_id = goal.id
                goal = SavingsGoal.objects.get(id=goal_id, user=request.user)

                Contribution.objects.create(
                    user=request.user,
                    goal=goal,
                    amount=amount,
                    date=datetime.datetime.now()
                )

                return redirect('progress')

            except SavingsGoal.DoesNotExist:
                return render(request, 'error.html', {'message': 'Goal not found.'})

    else:
        form = ContributionForm()

    return render(request, 'contribute.html', {'form': form})



@login_required
def update_goal(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk)
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('progress')
    else:
        form = SavingsGoalForm(instance=goal)
    return render(request, 'update_goal.html', {'form': form, 'goal': goal})


@login_required
def delete_goal(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk)
    if request.method == 'POST':
        goal.delete()
        return redirect('progress')
    return render(request, 'confirm_delete.html', {'goal': goal})

@login_required
def goal_detail(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk)
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.goal = goal
            contribution.user = request.user
            contribution.save()
            return redirect('goal_detail', pk=goal.pk)
    else:
        form = ContributionForm()
    return render(request, 'goal_detail.html', {'goal': goal, 'form': form})

@login_required
def progress_view(request):
    user = request.user
    goals = SavingsGoal.objects.filter(user=user)
    return render(request, 'progress.html', {'goals': goals})

def success(request):
    return render(request, 'success.html')

@login_required
def input_financial_data(request):
    if request.method == 'POST':
        form = FinancialDataForm(request.POST)
        if form.is_valid():
            # Save financial data to the user's profile or database
            # Assuming you have a user profile model to save this data
            user_profile = request.user.profile
            user_profile.income = form.cleaned_data['income']
            user_profile.expenses = form.cleaned_data['expenses']
            user_profile.savings = form.cleaned_data['savings']
            user_profile.save()
            return redirect('financial_insights')
    else:
        form = FinancialDataForm()
    return render(request, 'input_financial_data.html', {'form': form})

def financial_insights(request):
    # Retrieve financial data and generate insights
    user_profile = request.user.profile
    insights = calculate_insights(user_profile)
    tips = generate_tips(user_profile)
    return render(request, 'financial_insights.html', {'insights': insights, 'tips': tips})

def calculate_insights(user_profile):
    # Placeholder function to calculate insights
    return {
        'average_income': user_profile.income,
        'average_expenses': user_profile.expenses,
        'average_savings': user_profile.savings,
        'savings_comparison': user_profile.savings - (user_profile.income - user_profile.expenses)
    }

def generate_tips(user_profile):
    # Placeholder function to generate tips
    return [
        "Consider reducing your expenses by 10% to increase savings.",
        "Track your spending more closely."
    ]
