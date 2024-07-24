from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, SavingsGoalForm, ContributionForm
from .models import SavingsGoal, Contribution
from .utils import generate_recommendations
from django.contrib.auth.forms import AuthenticationForm
from .models import Goal, Contribution, SavingsGoal
import datetime
from django.conf import settings
import pandas as pd



def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('create_goal')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


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
def insights_view(request):
    user = request.user
    contributions = Contribution.objects.filter(user=user).values('amount', 'income', 'date', 'goal__status')
    df = pd.DataFrame(list(contributions))

    if df.empty:
        insights = ["No data available for insights."]
        tips = []
    else:
        # Detailed Insights and Tips Algorithm
        insights, tips = analyze_savings_behavior(df)

    return render(request, 'insights.html', {'insights': insights, 'tips': tips})

def analyze_savings_behavior(df):
    insights = []
    tips = []

    df['savings_rate'] = df['amount'] / df['income']
    avg_savings_rate = df['savings_rate'].mean()

    if avg_savings_rate < 0.2:
        insights.append("Your average savings rate is below the recommended rate.")
        tips.append("Try to save at least 20% of your income each month.")

    completed_goals = df[df['goal__status'] == 'completed']
    goal_completion_rate = len(completed_goals) / len(df)

    if goal_completion_rate < 0.8:
        insights.append("Your goal completion rate is below the recommended level.")
        tips.append("Set smaller, more achievable goals to improve your completion rate.")

    df['contribution_month'] = df['date'].apply(lambda x: x.strftime('%Y-%m'))
    monthly_contributions = df.groupby('contribution_month')['amount'].sum()

    if monthly_contributions.std() > 0.1 * monthly_contributions.mean():
        insights.append("Your savings contributions are irregular.")
        tips.append("Set up automatic transfers to ensure regular savings contributions.")

    return insights, tips


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
            goal.total_contributed += contribution.amount
            goal.save()
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
