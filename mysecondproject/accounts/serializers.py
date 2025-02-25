from rest_framework import serializers
from .models import CustomUser

'''
    serializers will convert the ExpenseModel objects to 
    a format (JSON) supported in the API
'''

class CustomUserSerializer(serializers.ModelSerializer): 
    '''
        Since we don't need to show any url'shere, we choose ModelSerializer instead of HyperlinkedModelSerializer
    '''

    class Meta: 
        model = CustomUser
        fields = '__all__'
        #fields = ['username', 'is_staff']