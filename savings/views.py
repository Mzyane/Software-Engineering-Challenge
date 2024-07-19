from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, SavingsGoalForm, ContributionForm
from .models import SavingsGoal, Contribution

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('create_goal')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    # Implement login logic
    pass

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
            contribution = form.save(commit=False)
            contribution.user = request.user
            contribution.save()
            return redirect('progress')
    else:
        form = ContributionForm()
    return render(request, 'contribute.html', {'form': form})

@login_required
def progress(request):
    goals = SavingsGoal.objects.filter(user=request.user)
    context = {'goals': goals}
    return render(request, 'progress.html', context)
