
from django.core.management.base import BaseCommand
from django.db import models  # Import models module here
from savings.models import Contribution, SavingsGoal

class Command(BaseCommand):
    help = 'Generate savings insights for users'

    def handle(self, *args, **options):
        goals = SavingsGoal.objects.all()

        for goal in goals:
            total_contributions = Contribution.objects.filter(goal=goal).aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0
            avg_contribution = Contribution.objects.filter(goal=goal).aggregate(avg_amount=models.Avg('amount'))['avg_amount'] or 0
            contribution_count = Contribution.objects.filter(goal=goal).count()
            progress_percentage = (total_contributions / goal.target_amount) * 100 if goal.target_amount else 0
            insights = []
            if avg_contribution < (goal.target_amount / 12):  # Example benchmark: saving at least 1/12 of the goal per month
                insights.append('Consider increasing your average monthly savings to stay on track.')

            if progress_percentage < 50:
                insights.append('You are less than halfway to your savings goal. Consider boosting your contributions.')

            goal.progress = progress_percentage
            goal.save()

            self.stdout.write(f'Insights for goal {goal.id}: {", ".join(insights)}')
