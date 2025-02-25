
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from expensetracker.views import HomeView
from rest_framework import routers
from api.views import ExpenseViewSet, CustomUserViewSet

router = routers.DefaultRouter()
router.register(r'expenses', ExpenseViewSet)
router.register(r'users', CustomUserViewSet )

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Built-in login view


 
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    #This is where my actual api endpoints are exposed: 
    path('api/', include(router.urls))
]
