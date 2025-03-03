# README

This project is my way of learning Django, little by little and concept by concept. As you will soon notice, my focus thus far has been on the backend. 

This README will act as a "note to self" for now, and I will take notes of different things I think about along the way. It may be ideas for future implemenation, or notes on how things work that might be obvious to the experienced user, but not for me (yet).
If the README grows out of control, I'll consider moving the notes elsewhere :smile: 

The code includes a lot of explanotary comments. It's because I am still learning and want to remember how things work, and why I have made the choices I have. 

## Prioritized to do list :sunglasses: 
1. Export API with same permission/accesss as POST and GET
2. Soft delete using DELETE api (now we have hard delete)
3. Use permission and groups to implement more fine grained control access
4. Logging of some sort 


## To do list :memo:
This is just a list of ideas. Might not be updated. Kind of a braindump. 

- customize the swagger doc
- have granular permissions for non admin users, making some of them (the "admin of an organization") able to see users from their own organization. 
    - same with expenses - filter by organization. 
    - then I need to make an organization model - need to have a think before implementing :think: 
- maybe create a permission so that staff users can see ALL expenses (if they have said permission)
- make it so that admin users can edit ALL expenses regardless of owner
- pagination 
- download your expenses as csv 
    - filter on month/year/other 
- I guess I need to add some front end stuff at some point :alien:

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

## Pagination

According to this [stackoverflow](https://stackoverflow.com/questions/46916128/how-do-you-paginate-a-viewset-using-a-paginator-class) it seems like global or custom pagination settings won't work with viewset :screem_cat:

## Swagger doc 

Should read a bit up on manual_parameters here. used to control the parameters shown in swagger doc UI

    @swagger_auto_schema(
            operation_description="Fetch expense data.",
            manual_parameters=[
                openapi.Parameter(
                    'month',  # Parameter name in URL
                    openapi.IN_QUERY,  # Query parameter
                    description="Filter expenses by month (1-12)",  
                    type=openapi.TYPE_INTEGER,  # Expecting an integer
                    required=False  # This makes it optional
                ),
            ]        
        )


## Things I've done :bowtie: 
These are items moved from the to do list because they have been implemented and I believe they are working. 

:white_check_mark: api/fileexport (api/views/exportview.py)

:beetle: Fixed POST api/users bug. 

:white_check_mark: filter user API on date_joined, date_of_birth or other (optional) parameters.

:white_check_mark: filter on month/year, aka: being able to call GET expenses and add some condition (year=2025) or something. 

:white_check_mark: consider separating the different API endpoints into separate files, and collecting them all in API 

:white_check_mark: give non admin users access to GET/PUT/DELETE own user information 

:white_check_mark: add some open (does not need authentication) APIs (list all expenses) 

:white_check_mark:require login or some authentication to be able to use the api 
- only admin /staff can access user-api's

:white_check_mark:only see the expenses you are the owner of (staff and non-staff) 

:white_check_mark: Need logout fucntionality for non-admin users (/logout). Right now they have no way of logging out. 

:white_check_mark: staff user with the right permission can see all expenses and delete them 

:white_check_mark:make it so that the owner of the expense is automatically set to the same user who posts it

## ChatGPT's suggestions for things to implement: 

**Backend-forbedringer:**
1. Brukerroller og tillatelser: Implementer grupper og tillatelser (f.eks. admin, regular_user) med Django sitt permissions-system. Bruk DRF-permissions til å begrense API-endepunkter basert på roller.
    - Eksempel: Bare administratorer kan slette utgifter.

2. Soft Delete for utgifter: I stedet for å slette poster fra databasen, legg til et is_deleted-felt og filtrer ut slettede elementer. Gir bedre feilhåndtering og mulighet for å gjenopprette data.
3. Logging og overvåkning: Logg API-kall med Django Signals. Bruk django-activity-stream for å spore hendelser som "bruker opprettet utgift". Implementer Sentry eller Elastic APM for feillogging.

**Utvid API-funksjonaliteten:**
4. Søk og filtrering: Bruk DjangoFilterBackend eller django-rest-framework-filters for å filtrere utgifter basert på dato, kategori osv.
    - eksempel: GET /api/expenses/?category=food&min_amount=100
5. Paginering: Hvis API-et returnerer mange utgifter, implementer paginering med PageNumberPagination eller LimitOffsetPagination.
6. Eksport av data: Gi brukere mulighet til å eksportere utgifter som CSV eller Excel (bruk django-import-export eller pandas). Kan kombineres med e-postvarsling (f.eks. send eksporterte data som vedlegg).

**Frontend & UI (Django + JavaScript/React)**
7. Enkel frontend med Django Templates: Bygg en enkel visuell oversikt over utgiftene med Django Template Engine. Bruk HTMX for AJAX-oppdateringer uten å bruke et frontend-rammeverk.
8. Bygg en React/Vue-app: Lag en frontend med React eller Vue som henter utgifter fra API-et ditt. Bruk React Query eller Axios for API-kall.

**Autentisering og Sikkerhet**
9. OAuth eller Google/Facebook login: Bruk django-allauth eller dj-rest-auth for å la brukere logge inn med Google/Facebook.
10. Rate Limiting og Throttling: Bruk DRF-throttling for å begrense API-kall og forhindre misbruk.
11. Totrinnsautentisering (2FA): Bruk django-otp eller django-two-factor-auth for ekstra sikkerhet.

**Andre mulige funksjoner:**
12. Automatiske e-poster: Bruk Celery + Redis for å sende periodiske rapporter om utgifter til brukerne.
13. Dashboards & Statistikk: Bruk django-plotly-dash eller matplotlib for å visualisere utgifter med grafer.
14. AI/ML-integrasjon: Bruk scikit-learn for å gi innsikt i utgiftsvaner eller predikere kommende utgifter.

## How to add a new custom field to the CustomUser model in accounts: 
    1. add it in models.py
    2. update forms.py
    3. update admin.py (add fieldsets and add_fieldsets)
    4. run migrations
    5. restart server and test it