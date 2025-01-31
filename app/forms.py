from django import forms
from .models import Budget, Expense

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'total_amount', 'start_date', 'end_date']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount']
