# README

In this project we will try to build a custom user model from the start of the project (to avoid manual migration later on). 

In this readme file we will collect what we learn along the way. 

## How to add a new custom field to the CustomUser model in accounts: 
    1. add it in models.py
    2. update forms.py
    3. update admin.py (add fieldsets and add_fieldsets)
    4. run migrations
    5. restart server and test it


## Plan: 
1. add some open (does not need authentication) APIs (list all expenses)
2. require login or some authentication to be able to use the api
3. only see the expenses you are the owner of 