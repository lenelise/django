from expensetracker.models import Income
from expensetracker.serializers import IncomeGetSerializer,IncomePostSerializer

from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.db.models import Q
import logging

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
    ''' CRUD APIs for the Income model. 
        Same permission rules as for the Expense model. 
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
        pk = kwargs.get('pk', None)

        if pk is None: 
            logger.info(f"GET api/income called by userid {self.request.user.id} with no income id given")
            incomes = self.get_queryset()
            serializer = IncomeGetSerializer(incomes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else: 
            logger.info(f"GET api/income called by userid {self.request.user.id} with income_id {pk}")
            income = Income.objects.get(pk=pk)
            serializer = IncomeGetSerializer(income)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_description="Post new category data." ) 
    def post(self, request): 
        logger.info(f"POST api/income called by userid {self.request.user.id}.")
        serializer = IncomePostSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            logger.warning("POST api/income, serializer not valid.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, **kwargs):
        logger.info(f"PUT api/income called by userid {self.request.user.id} with income_id {pk}")
        pk = kwargs.get('pk', None)

        if not pk:
            logger.warning("PUT api/income: primary key not given.")
            return Response({"detail": "Primary key is required"}, status=status.HTTP_400_BAD_REQUEST)

        #you can only edit your own expense:
        try:
            income = Income.objects.get(pk=pk, owner = request.user)
        except Income.DoesNotExist:
            logger.error(f"PUT api/income: task with id {pk} not found.")
            raise NotFound(detail="Task not found, or has other owner")
        serializer =  IncomePostSerializer(income, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: 
            logger.warning("POST api/income: serializer not valid.")
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
           

    @swagger_auto_schema(
            operation_description="Remove an income."        
    )
    def delete(self, *args, **kwargs):
        logger.info(f"DELETE api/income called by userid {self.request.user.id}")
        if self.request.user.is_staff: 
            return super().destroy(self.request,*args, **kwargs)
        else: 
            logger.warning("DELETE api/income: non admin user tried to delete.")
            return Response("This action is not allowed for non-staff users", status=status.HTTP_403_FORBIDDEN)

