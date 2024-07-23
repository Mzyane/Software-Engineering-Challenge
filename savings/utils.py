import datetime
from .models import SavingsGoal

def generate_recommendations(user):
    goals = SavingsGoal.objects.filter(user=user)
    recommendations = []

    if not goals:
        return ["You currently have no savings goals. Consider setting some to start saving!"]

    today = datetime.datetime.now().date()
    for goal in goals:
        if goal.target_amount > 1000:
            recommendations.append(
                f"Consider setting a monthly savings target for your goal: {goal.name}."
            )
        if goal.target_date and goal.target_date < today + datetime.timedelta(days=30):
            recommendations.append(
                f"You are approaching the deadline for goal: {goal.name}. Increase your contributions!"
            )

    if not recommendations:
        recommendations.append("Keep up the good work with your savings goals!")

    return recommendations
