from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.filters import CustomUserFilter
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer, CustomUserPostSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        params = {
            "username": self.request.query_params.get("username"),
            "date_joined__month": self.request.query_params.get('month_joined'),
            "is_staff": self.request.query_params.get('is_staff')
        }

        query = Q(is_deleted=False) # only want to list non-deleted users

        if not self.request.user.is_staff:
            #non admin users should only see their own user information no matter the query params
            query &= Q(id=self.request.user.id)
        else: 
            #admin users can see all, or filter out any user they want
            for key,value in params.items():
                if value: 
                    query &= Q(**{key:value})
        
        return CustomUser.objects.filter(query)

    #overriding get_serializer_class since we have different serializers for GET and POST
    def get_serializer_class(self): 
        if self.action in ['create', 'update']: 
            return CustomUserPostSerializer
        else: 
            return CustomUserSerializer
          
    @swagger_auto_schema(
        operation_description="Fetch user data. Admin get all user data unless pk is given, non admin get own user data.",
        manual_parameters=[
            openapi.Parameter(
                'month_joined',  # Parameter name in URL
                openapi.IN_QUERY,  # Query parameter
                description="Filter users by month joined (01-12)",  
                type=openapi.TYPE_INTEGER,  # Expecting an integer
                required=False  # This makes it optional
            ),
        ]       
    ) 
    def list(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None) #if no pk is given it defaults to None

        if pk: 
            try:
                user = CustomUser.objects.get(pk=pk)
            except CustomUser.DoesNotExist:
                raise NotFound(detail="User not found, or has other owner")
            serializer =  CustomUserSerializer(user, context={"request": request})
        else: 
            users = self.get_queryset()
            serializer = CustomUserSerializer(users, many=True, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create users. Only available for admin users."        
    )    
    def create(self, request, *args, **kwargs):
        serializer = CustomUserPostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            if self.request.user.is_staff:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Forbidden - you don't have access to this operation."}, status=status.HTTP_403_FORBIDDEN)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description = "Hard delete user (note that option for soft_delete exists)."      
    ) 
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else: 
            return super().destroy(self.request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Soft delete user"       
    ) 
    @action(detail=True) #detail=True means the action is done on one object, not all. Primary key is required. 
    def soft_delete(self, request, **kwargs):
        pk = kwargs.get('pk', None) #get the pk if it is given, if not set to None

        if pk is None: 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else: 
            user = CustomUser.objects.get(pk=pk)
            user.is_deleted = True
            user.is_active = False
            user.groups = [] #remove all permissions given via groups
            user.user_permissions = [] #remove all permissions
            user.save() 
            return Response(status=status.HTTP_200_OK)
