from django.contrib import admin
from .models import Expense, ExpenseCategory, Income, Budget

# Register your models here.

admin.site.register(Expense)
admin.site.register(ExpenseCategory)
admin.site.register(Income)
admin.site.register(Budget)