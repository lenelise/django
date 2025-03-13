from datetime import datetime
from expensetracker.models import Expense, Income, Budget
from accounts.models import CustomUser
from django.db import connection

def run():
    # #Create new row
    user = CustomUser.objects.filter(username = "fnugg").first()

    # Budget.objects.create(
    #     title="My monthly budget",
    #     note = "My regular expenses for a regular month",
    #     owner = user
    # )

    # #Get all rows from a table
    # budgets = Budget.objects.all()
    # print(budgets)

    # #Get first object
    # budget = Budget.objects.first()
    # print(budget)

    # #indexing
    # budget = Budget.objects.all()[1]
    # print(budget)

    # #Filter
    # budget = Budget.objects.filter(id=1)
    # expenses = Expense.objects.filter(owner_id = 3)
    # expenses = Expense.objects.filter(owner_id__lte = 3)
    # expenses = Expense.objects.filter(owner_id__gte = 3)
    # expenses = Expense.objects.exclude(owner_id = 4) #returns everything except the condition

    # #count
    # print(Budget.objects.count())

    # #Querying foreign key
    # budget = Budget.objects.filter(id=1)[0]
    # expense = Expense.objects.create(
    #     title="New Expense",
    #     owner = user, 
    #     budget = budget,
    #     price  = 100, 
    #     date = '2025-03-13'
    # )

    # # Changing existing records
    # expense = expenses[0]
    # print(expense.title)
    # expense.title = "new name"
    # expense.save() #without this line, the db is not actually updated
    # print(expense.title)

    # INNER JOIN budget and expenses:
    # budget = Budget.objects.first()
    # print(budget.expenses.all()) #by default it should have been expense_set, but expenses is the related name (model.py)

    # GET OR CREATE
    # creates a new record of it cannot find it
    # expense = Expense.objects.first()

    # budget = Budget.objects.get_or_create(
    #     title = "April Budget"
    # )

    # print(budget)   

    # print(connection.queries) #print all SQL queries in script
