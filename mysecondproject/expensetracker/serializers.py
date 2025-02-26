from rest_framework import serializers
from .models import Expense

'''
    serializers will convert the ExpenseModel objects to 
    a format (JSON) supported in the API
'''

class ExpenseSerializer(serializers.HyperlinkedModelSerializer): 
    '''
        Choosing HyperlinkedModelSerializer instead of ModelSerializer because we want to include
        urls to resources in the API response, instead of just the primary key. 
        Ex: url to user, not just the user id. 
    '''

    class Meta: 
        model = Expense
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            """
            Override the constructor to remove the 'owner' field when creating a new expense.
            """
            super().__init__(*args, **kwargs)
            
            # Remove the 'owner' field for the create method to prevent it from being included in the form.
            if self.context['request'].method == 'POST':
                self.fields.pop('owner')