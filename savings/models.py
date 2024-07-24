from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.conf.urls.static import static


class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_contributed = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    target_date = models.DateField()

    @property
    def remaining_amount(self):
        return self.target_amount - self.total_contributed
    def calculate_total_contributed(self):
        from django.db.models import Sum
        total_contributed = Contribution.objects.filter(goal=self).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        return total_contributed

    def save(self, *args, **kwargs):
        self.total_contributed = self.calculate_total_contributed()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Contribution(models.Model):
    goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} contributed {self.amount} to {self.goal.name}"

class SavingsContribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey('SavingsGoal', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

class SavingsInsights(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    average_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    contribution_frequency = models.DurationField()
    goal_progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    tips = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
