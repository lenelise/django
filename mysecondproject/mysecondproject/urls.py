
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from expensetracker.views import HomeView
from api.views.expenseviewset import ExpenseViewSet
from api.views.customuserviewset import CustomUserViewSet
from api.views.exportview import ExportView
from api.views.categoryview import ExpenseCategoryView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import routers, permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

#For Swagger: 
schema_view = get_schema_view(
   openapi.Info(
      title="Mysecondproject API's",
      default_version='v1',
      description="These are the available API's for mysecondproject. ",
   ),
   public=True,
   permission_classes=(permissions.IsAuthenticated,),
)

#router required since we use ViewSets for API endpoints: 
router = routers.DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense') #basename because we override get_queryset in the view
router.register(r'users', CustomUserViewSet, basename='customuser')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Built-in login view
    path('logout/', auth_views.LogoutView.as_view(http_method_names=['get', 'post']), name='logout'),  # Built-in logout view
   
    #This is where my actual api endpoints are exposed: 
    path('api/', include(router.urls), name="api"), 
    path('api-auth/', include('rest_framework.urls')), #login/out option in browsable API UI
    path('api/fileexport/', ExportView.as_view(), name='file-export'), 
    path('api/categories/', ExpenseCategoryView.as_view(), name='category'),

    #JWT authentication:
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    #Swagger: 
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
    #path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
