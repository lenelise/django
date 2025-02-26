# README

In this project we will try to build a custom user model from the start of the project (to avoid manual migration later on). 

This README will act as a "note to self" for now, and I will take a note of different things: 
- who I did it
- what I want to do 
- any other thought that I feel like writing down somewhere. 

If it grows out of control, I'll consider moving the notes elsewhere :smile: 

## How to add a new custom field to the CustomUser model in accounts: 
    1. add it in models.py
    2. update forms.py
    3. update admin.py (add fieldsets and add_fieldsets)
    4. run migrations
    5. restart server and test it

## API and restrictions:
- you need to be logged in to access any of the APIs
- only staff/admin users can access api/users
- staff and non-staff users can both access api/expenses

## To do: 
1. add some open (does not need authentication) APIs (list all expenses) :white_check_mark:
2. require login or some authentication to be able to use the api :white_check_mark:
    - only admin /staff can access user-api's
3. only see the expenses you are the owner of (staff and non-staff) :white_check_mark:
4. staff user with the right permission can see all expenses and delete them 
5. maybe create a permission so that staff users can see ALL expenses (if they have said permission)
6. Need logout fucntionality for non-admin users (/logout). Right now they have no way of logging out :white_check_mark:
7. make it so that the owner of the expense is automatically set to the same user who posts it