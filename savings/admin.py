from django.contrib import admin
from .models import SavingsGoal, Contribution

class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_amount', 'total_contributed', 'target_date', 'remaining_amount')
    search_fields = ('name',)
    list_filter = ('target_date',)

class ContributionAdmin(admin.ModelAdmin):
    list_display = ('goal', 'amount', 'date', 'user')
    list_filter = ('date', 'user')
    search_fields = ('goal__name', 'user__username')

class GoaldetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_amount', 'total_contributed', 'target_date', 'remaining_amount')
    search_fields = ('name',)
    list_filter = ('target_date',)

admin.site.register(SavingsGoal, SavingsGoalAdmin)
admin.site.register(Contribution, ContributionAdmin)
