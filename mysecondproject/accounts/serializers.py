from rest_framework import serializers
from .models import CustomUser

'''
    serializers will convert the CustomUserModel objects to a format supported in the API (JSON) 
'''

class CustomUserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = CustomUser
        fields = '__all__'
        # fields = ['username', 'password', 'user_permissions', 'is_staff']

class CustomUserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 
            'password', 
            'first_name', 
            'last_name',
            'date_of_birth']