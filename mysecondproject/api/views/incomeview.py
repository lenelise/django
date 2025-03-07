from rest_framework.views import APIView
from expensetracker.models import Income
from expensetracker.serializers import IncomeGetSerializer,IncomePostSerializer
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.exceptions import NotFound


from rest_framework import permissions, status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import logging

'''
Note to self: Using the class based view approach, we will have one class for each API endpoint. 
Core difference from ViewSets where you have one class per model, and then one class method
for each endpoint. 
'''

logger = logging.getLogger(__name__)

@swagger_auto_schema(
    operation_description="Fetch income data.",
    manual_parameters=[
        openapi.Parameter(
            'month',  # Parameter name in URL
            openapi.IN_QUERY,  # Query parameter
            description="Filter income by month (1-12)",  
            type=openapi.TYPE_INTEGER,  # Expecting an integer
            required=False  # This makes it optional
        ),
        openapi.Parameter(
            'owner',  # Parameter name in URL
            openapi.IN_QUERY,  # Query parameter
            description="Filter income by owner userid.",  
            type=openapi.TYPE_INTEGER,  # Expecting an integer
            required=False  # This makes it optional
        )
    ]        
)
class IncomeView(APIView):
    '''
        non admins should see own income. 
        admins should see all. 
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = Q()         
        params = {
            "date__year" : self.request.query_params.get('year'),
            "date__month" : self.request.query_params.get('month'),
            "owner": self.request.query_params.get('owner')
        }

        for key,value in params.items(): 
            if value:
                query &= Q(**{key: value})

        #adding this to retrict non admin users to their own expeses only:
        if not self.request.user.is_staff:
            query &= Q(owner=self.request.user)
        
        return Income.objects.filter(query)
    
    def get_serializer_class(self): 
        if self.action in ['create', 'update']:
            return IncomePostSerializer
        else:
            return IncomeGetSerializer


    @swagger_auto_schema(operation_description="Fetch all income data ." ) 
    def get(self, request, **kwargs): 
        logger.info("Entering GET income")
        pk = kwargs.get('pk', None)

        if pk is None: 
            # incomes = Income.objects.all()
            logger.info("GET income: no pk given")
            incomes = self.get_queryset()
            serializer = IncomeGetSerializer(incomes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else: 
            logger.error("GET income: pk given")
            income = Income.objects.get(pk=pk)
            serializer = IncomeGetSerializer(income)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_description="Post new category data." ) 
    def post(self, request): 
        serializer = IncomePostSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, **kwargs):
        pk = kwargs.get('pk', None)

        if not pk: 
            return Response({"detail": "Primary key is required"}, status=status.HTTP_400_BAD_REQUEST)

        #you can only edit your own expense:
        try:
            income = Income.objects.get(pk=pk, owner = request.user)
        except Income.DoesNotExist:
            raise NotFound(detail="Task not found, or has other owner")
        serializer =  IncomePostSerializer(income, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: 
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
           

    @swagger_auto_schema(
            operation_description="Remove an income."        
    )
    def delete(self, *args, **kwargs):
        if self.request.user.is_staff: 
            return super().destroy(self.request,*args, **kwargs)
        else: 
            return Response("This action is not allowed for non-staff users", status=status.HTTP_403_FORBIDDEN)

