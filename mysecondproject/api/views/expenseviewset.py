from django.db.models import Q

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from expensetracker.models import Expense
from expensetracker.serializers import ExpenseGetSerializer, ExpensePostSerializer

import logging

logger = logging.getLogger(__name__)

class ExpenseViewSet(viewsets.ModelViewSet):
    '''
        GET: non staff users can see own expenses, admin users can see all. 
        POST: same behavior for all, you can only add expenses to yourself. 
        PUT: non staff users can edit own expenses, admins can edit all. 
        DELETE: non admin user cannot delete expenses, admin users can delete any expense. 
    '''
    # overriding parent get_queryset method to restrict what they see
    # means we need basename in url.py routers

    permission_classes = [permissions.IsAuthenticated]
    # fitlerset_fields = ('title')
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
        
        return Expense.objects.filter(query)
    
    def get_serializer_class(self): 
        if self.action in ['create', 'update']:
            return ExpensePostSerializer
        else:
            return ExpenseGetSerializer


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
            openapi.Parameter(
                'owner',  # Parameter name in URL
                openapi.IN_QUERY,  # Query parameter
                description="Filter expenses by owner userid.",  
                type=openapi.TYPE_INTEGER,  # Expecting an integer
                required=False  # This makes it optional
            )
        ]        
    )
    def list(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None) #if no pk is given it defaults to None

        if pk: 
            try:
                logger.info(f"GET api/expenses called by userid {self.request.user.id} with expense_id {pk}")
                expense = Expense.objects.get(pk=pk, owner = request.user)
            except Expense.DoesNotExist:
                logger.error("GET api/expense: expense do not exist")
                raise NotFound(detail="Task not found, or has other owner")
            serializer =  ExpenseGetSerializer(expense, context={"request": request})
        else: 
            logger.info(f"GET api/expenses called by userid {self.request.user.id} with no expense_id")
            expenses = self.get_queryset()
            serializer = ExpenseGetSerializer(expenses, many=True, context={"request": request})
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create expense(s)."        
    )    
    def create(self, request, *args, **kwargs):
        serializer = ExpensePostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            logger.info(f"POST api/expenses called by userid {self.request.user.id}: success")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"POST api/expenses called by userid {self.request.user.id} but was bad")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update existing expense data."        
    )    
    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None) #if no pk is given it defaults to None
        logger.info(f"PUT api/expense called by userid {self.request.user.id} with expenseid {pk}")

        # If no pk given we throw an error:
        if not pk: 
            logger.warning("PUT api/expense: primary key not given.")
            return Response({"detail": "Primary key is required"}, status=status.HTTP_400_BAD_REQUEST)

        #you can only edit your own expense:
        try:
            expense = Expense.objects.get(pk=pk, owner = request.user)
        except Expense.DoesNotExist:
            logger.error(f"PUT api/expense: task with id {pk} not found.")
            raise NotFound(detail="Task not found, or has other owner")
        
        #the actual editing: 
        serializer =  ExpensePostSerializer(expense, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: 
            logger.warning("POST api/expense: serializer not valid.")
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
           
    @swagger_auto_schema(
            operation_description="Remove an expense."        
    )
    def destroy(self, *args, **kwargs):
        logger.info(f"DELETE api/expense called by userid {self.request.user.id}")
        if self.request.user.is_staff: 
            return super().destroy(self.request,*args, **kwargs)
        else: 
            logger.warning("DELETE api/expense: non admin user tried to delete.")
            return Response("This action is not allowed for non-staff users", status=status.HTTP_403_FORBIDDEN)



       
