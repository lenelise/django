# README

This project is my way of learning Django, little by little and concept by concept. As you will soon notice, my focus thus far has been on the backend. 

This README will act as a "note to self" for now, and I will take notes of different things I think about along the way. It may be ideas for future implemenation, or notes on how things work that might be obvious to the experienced user, but not for me (yet).
If the README grows out of control, I'll consider moving the notes elsewhere :smile: 

The code includes a lot of explanotary comments. It's because I am still learning and want to remember how things work, and why I have made the choices I have. 

## How to add a new custom field to the CustomUser model in accounts: 
    1. add it in models.py
    2. update forms.py
    3. update admin.py (add fieldsets and add_fieldsets)
    4. run migrations
    5. restart server and test it

## API's and restrictions:
All API's can be found on `base_url/swagger`. Be aware of the fact that we have not done much to customize this page (yet). The documentation is made using [Yet another swagger generator.](https://drf-yasg.readthedocs.io/en/stable/readme.html#quickstart)

**/api/expenses:**

Non-admin users can only see their own expenses. Admin users can see all regardless of owner. 
All users can post new expenses, and they are automatically added as owner to that exspense. 

Only admin users can DELETE expenses. 

Users can only edit their own expenses. 

**/api/users:**

This API endpoint is only available for admin users. 

## JWT authentication for API requests:
We have used [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) to add JWT authentication for API requests. 

We have kept the option to have browsable API's, and thus also Session based authentication. 

A testing script for JWT authentication is httptest.py. It is just a script we have used during development to test the feature (and debugging a very annoying :beetle:), nothing more or nothing less. 

## Logging
Added something in settings, but honestly not sure what it does at the moment (or if it does anything at all). Need to read up on this. 


## To do list/braindump
This is just a list of ideas. Might not be updated. Kind of a braindump. 

- customize the swagger doc
- have non admin users be able to GET their own user information, but not others
- have granular permissions for non admin users, making some of them (the "admin of an organization") able to see users from their own organization. 
    - same with expenses - filter by organization. 
    - then I need to make an organization model - need to have a think before implementing :think: 
- maybe create a permission so that staff users can see ALL expenses (if they have said permission)
- make it so that admin users can edit ALL expenses regardless of owner
- consider separating the different API endpoints into separate files, and collecting them all in API 
- pagination 
- download your expenses as csv 
    - filter on month/year/other 
- I guess I need to add some front end stuff at some point :alien:

## Prioritized to do list :sunglasses: 
1. give non admin users access to view/GET own user information 
2. pagination expenses (in API repsonse mainly, since we basically have no front end yet)
3. filter on month/year, aka: being able to call GET expenses and add some condition (year=2025) or something. 

## Done: 
These are items moved from the to do list because they have been implemented and we believe they are working. 

:white_check_mark: add some open (does not need authentication) APIs (list all expenses) 

:white_check_mark:require login or some authentication to be able to use the api 
- only admin /staff can access user-api's

:white_check_mark:only see the expenses you are the owner of (staff and non-staff) 

:white_check_mark: Need logout fucntionality for non-admin users (/logout). Right now they have no way of logging out. 

:white_check_mark: staff user with the right permission can see all expenses and delete them 

:white_check_mark:make it so that the owner of the expense is automatically set to the same user who posts it

## ChatGPT's suggestions for things to implement: 
I asked ChatGPT what they would suggest for this project going forward. Here's what they said: 

1. Async tasks with Celery
2. Advanced authentication with JWT
3. Database optimization and indexing: 
    - note to self: change to postgreSQL?
4. API rate limiting and throttling
5. Implement caching strategies for data intenstive/read heavy operations
5. Docker and containarization
6. Deploy to prod

