from rest_framework import serializers
from .models import Expense, ExpenseCategory


class ExpenseGetSerializer(serializers.HyperlinkedModelSerializer): 
    class Meta: 
        model = Expense
        fields = '__all__'


class ExpensePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        exclude = ['owner']

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError(
                "Price must be greater than 0"
            )
        else: 
            return price

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = ExpenseCategory
        fields = '__all__'