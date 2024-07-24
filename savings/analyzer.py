import pandas as pd

class SavingsBehaviorAnalyzer:
    def __init__(self, data):
        self.data = data
        self.df = pd.DataFrame(data)

    def calculate_averages(self):
        avg_income = self.df['income'].mean()
        avg_expenses = self.df['expenses'].mean()
        avg_savings = self.df['savings'].mean()
        return {'avg_income': avg_income, 'avg_expenses': avg_expenses, 'avg_savings': avg_savings}

    def identify_high_expense_categories(self):
        categories = self.df.columns[2:]
        high_expense_categories = {cat: self.df[cat].mean() for cat in categories if self.df[cat].mean() > self.df['expenses'].mean()}
        return high_expense_categories

    def compare_savings_to_target(self, target_savings):
        actual_savings = self.df['savings'].mean()
        if actual_savings < target_savings:
            return f"Your actual savings are {target_savings - actual_savings} below your target savings."
        elif actual_savings > target_savings:
            return f"Your actual savings are {actual_savings - target_savings} above your target savings."
        else:
            return "Your savings are exactly at the target."

    def generate_insights_and_tips(self):
        insights = {}
        tips = []

        avg_data = self.calculate_averages()
        high_expenses = self.identify_high_expense_categories()
        savings_comparison = self.compare_savings_to_target(avg_data['avg_savings'] * 1.2)

        insights['average_income'] = avg_data['avg_income']
        insights['average_expenses'] = avg_data['avg_expenses']
        insights['average_savings'] = avg_data['avg_savings']
        insights['savings_comparison'] = savings_comparison

        if high_expenses:
            tips.append("Consider reducing expenses in high spending categories.")
            for category, amount in high_expenses.items():
                tips.append(f"Reduce {category} expenses by {amount * 0.1:.2f} to save more.")

        return {'insights': insights, 'tips': tips}
