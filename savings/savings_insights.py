from datetime import datetime
from django.utils.timezone import make_aware
from .models import Contribution, SavingsGoal, SavingsInsights, timedelta

def calculate_savings_insights(user):
    # Fetch user's contributions and goals
    contributions = Contribution.objects.filter(user=user)
    goals = SavingsGoal.objects.filter(user=user)

    # Calculate total savings
    total_savings = contributions.aggregate(total=models.Sum('amount'))['total'] or 0

    # Calculate average contribution amount
    average_contribution = contributions.aggregate(avg=models.Avg('amount'))['avg'] or 0

    # Calculate contribution frequency
    if contributions.count() > 1:
        dates = [c.date for c in contributions]
        intervals = [(dates[i] - dates[i-1]).total_seconds() for i in range(1, len(dates))]
        average_interval = sum(intervals) / len(intervals)
        contribution_frequency = timedelta(seconds=average_interval)
    else:
        contribution_frequency = timedelta(days=0)

    # Calculate goal progress
    goal_progress = 0
    for goal in goals:
        goal_contributions = contributions.filter(goal=goal)
        goal_total = goal_contributions.aggregate(total=models.Sum('amount'))['total'] or 0
        if goal.target_amount > 0:
            goal_progress = max(goal_progress, (goal_total / goal.target_amount) * 100)

    # Generate tips
    tips = generate_tips(total_savings, average_contribution, contribution_frequency, goal_progress)

    # Update or create insights
    insights, created = SavingsInsights.objects.update_or_create(
        user=user,
        defaults={
            'total_savings': total_savings,
            'average_contribution': average_contribution,
            'contribution_frequency': contribution_frequency,
            'goal_progress': goal_progress,
            'tips': tips
        }
    )

def generate_tips(total_savings, avg_contribution, frequency, goal_progress):
    tips = []
    if avg_contribution < 100:  # Example threshold
        tips.append("Consider increasing your average contribution amount to reach your goals faster.")
    if frequency > timedelta(days=30):  # Example threshold
        tips.append("You might benefit from more frequent contributions.")
    if goal_progress < 50:  # Example threshold
        tips.append("You are less than halfway to your goal. Consider increasing your contributions.")

    return "\n".join(tips)
