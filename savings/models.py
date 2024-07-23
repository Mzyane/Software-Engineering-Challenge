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

class Contribution(models.Model):
    goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} contributed {self.amount} to {self.goal.name}"

class Goal(models.Model):
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class SavingsContribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey('SavingsGoal', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
