from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, SavingsGoalForm, ContributionForm
from .models import SavingsGoal, Contribution
from .utils import generate_recommendations
from django.contrib.auth.forms import AuthenticationForm
from .models import Contribution, SavingsGoal
import datetime
from django.conf import settings


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

def goal_summary(request):
    goals = SavingsGoal.objects.all()
    insights = []

    for goal in goals:
        # Fetch insights based on the latest data
        insights.append({
            'goal': goal,
            'progress': goal.progress,
            'recommendations': generate_recommendations(goal)
        })

    return render(request, 'goal_summary.html', {'insights': insights})

def generate_recommendations(goal):
    recommendations = []
    # Example recommendations
    if goal.progress < 50:
        recommendations.append('You should increase your monthly contributions to reach your goal.')
    return recommendations
