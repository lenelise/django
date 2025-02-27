from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.

class Expense(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(blank=True) #optional to fill this out
    price = models.IntegerField(validators=[MinValueValidator(0)])
    owner = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self): 
        return str(self.title) + ": " + str(self.price) + '.'
    