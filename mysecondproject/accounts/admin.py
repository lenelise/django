from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin): 
    '''
        Since we are using a custom user model, we need to add the forms to edit and create
        new users here in this class. See forms.py for the forms. 
    '''

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    #Controls what fields are shown in the user list in admin portal:
    list_display = [
        "username",
        "email",
        "date_of_birth",
        "is_staff",
        "is_active"
    ]

    #controls how fields are grouped and displayed when editing an existing user in admin portal: 
    fieldsets = (
        *UserAdmin.fieldsets,  # Keep default fields
        ('Additional Info', {'fields': ('date_of_birth',)}),
    )

    #controls how fields are shown when adding a NEW user in django admin:
    add_fieldsets = ((None,{
        "classes": ("wide",),
        "fields": (
            "username",
            "email", 
            "date_of_birth", 
            "password1", 
            "password2"),
            },),)

admin.site.register(CustomUser, CustomUserAdmin)