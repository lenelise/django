from rest_framework import serializers
from .models import Expense

'''
    serializers will convert the ExpenseModel objects to 
    a format (JSON) supported in the API

    Since we want different fields in GET and POST, we need two separate serializer classes

'''

class ExpenseGetSerializer(serializers.HyperlinkedModelSerializer): 
    '''
        Choosing HyperlinkedModelSerializer instead of ModelSerializer because we want to include
        urls to resources in the API response, instead of just the primary key. 
        Ex: url to user, not just the user id. 
    '''

    class Meta: 
        model = Expense
        fields = '__all__'


class ExpensePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        # fields = ['title', 'content', 'price']
        exclude = ['owner']

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError(
                "Price must be greater than 0"
            )
        else: 
            return price
