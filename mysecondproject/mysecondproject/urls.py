
from django.contrib import admin
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

    # 
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    #This is where my actual api endpoints are exposed: 
    path('api/', include(router.urls))
]
