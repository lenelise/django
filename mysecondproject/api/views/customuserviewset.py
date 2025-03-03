from django.db.models import Q

from rest_framework import viewsets,permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer, CustomUserPostSerializer

class CustomUserViewSet(viewsets.ModelViewSet):

    # queryset = CustomUser.objects.all() #we dont use this since we want different behavior depending on admin/non admin 
    # serializer_class = CustomUserSerializer #we dont use this, since we have mulitple CustomUser serializers

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        #query parameters: 

        params = {
            "date_joined__month": self.request.query_params.get('month_joined'),
            "is_staff": self.request.query_params.get('is_staff')
        }

        query = Q()

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
                raise NotFound(detail="Task not found, or has other owner")
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
