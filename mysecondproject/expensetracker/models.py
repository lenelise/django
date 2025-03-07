from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.

class Expense(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(blank=True) #optional to fill this out
    price = models.IntegerField(validators=[MinValueValidator(0)])
    owner = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE) #we dont want to keep the expense if the owner is deleted
    date = models.DateField()
    category = models.ForeignKey('ExpenseCategory', on_delete=models.SET_NULL, null=True) #we want to keep the expense if the category is deleted
    
    def __str__(self): 
        return str(self.title) + ": " + str(self.price) + '.'
    
class ExpenseCategory(models.Model): 
    title = models.CharField(max_length=50)
    
    def __str__(self): 
        return str(self.title)
    
class Income(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(blank=True) #optional to fill this out
    price = models.IntegerField(validators=[MinValueValidator(0)])
    owner = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE) #we dont want to keep the expense if the owner is deleted
    date = models.DateField()

    def __str__(self):
        return str(self.title) + ":" + str(self.price) + "."