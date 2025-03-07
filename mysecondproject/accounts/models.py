from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    '''
        Right now, this class is a subclass of AbstractUser.
        But also behaves identically as the default user model. 

        Fields in default user: 
            username
            first_name
            last_name
            email
            password
            groups
            user_permissions
            is_staff
            is_active
            is_superuser
            last_login
            date_joined
    '''

    #Trying to add an extra field: 
    date_of_birth = models.DateField(null=True) #if null=False we wouldn't be able to add the field since users already exists in db
    # password = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    # access_level = models.IntegerChoices(default=0)
    # password2 = models.CharField(max_length=255)
    
    def __str__(self):
        return self.username