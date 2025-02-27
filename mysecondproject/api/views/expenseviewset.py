from rest_framework import viewsets,permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from drf_yasg.utils import swagger_auto_schema

from expensetracker.models import Expense
from expensetracker.serializers import ExpenseGetSerializer, ExpensePostSerializer
# from accounts.models import CustomUser
# from accounts.serializers import CustomUserSerializer, CustomUserPostSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    '''
        GET: non staff users can see own expenses, admin users can see all. 
        POST: same behavior for all, you can only add expenses to yourself. 
        PUT: non staff users can edit own expenses, admins can edit all. 
        DELETE: non admin user cannot delete expenses, admin users can delete any expense. 
    '''
    permission_classes = [permissions.IsAuthenticated]
    # queryset = Expense.objects.all()  #a reference point, will be edited in method get_queryset() below
    # serializer_class = ExpensePostSerializer #overriding get_serializer_class instead, since we have multiple serializers


    # overriding parent get_queryset method to restrict what they see
    # means we need basename in url.py routers
    def get_queryset(self):
        '''
        Returns an iterable of objects from the database.
        Provides the data that will be used in POST, GET, PUT and DELETE. 
        '''
        if self.request.user.is_staff == False:
            return Expense.objects.filter(owner=self.request.user)
        else: 
            return Expense.objects.all()
    
    #overriding get_serializer_class since we have different serializers for GET and POST
    def get_serializer_class(self): 
        if self.action in ['create', 'update']:
            return ExpensePostSerializer
        else:
            return ExpenseGetSerializer

    ############################################
    # POST, GET, DELETE and PUT methods below: #
    ############################################

    @swagger_auto_schema(
        operation_description="Fetch expense data."        
    )
    def list(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None) #if no pk is given it defaults to None

        if pk: 
            try:
                expense = Expense.objects.get(pk=pk, owner = request.user)
            except Expense.DoesNotExist:
                raise NotFound(detail="Task not found, or has other owner")
            serializer =  ExpenseGetSerializer(expense, context={"request": request})
        else: 
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update existing expense data."        
    )    
    def update(self, request, *args, **kwargs):

        pk = kwargs.get('pk', None) #if no pk is given it defaults to None

        # If no pk given we throw an error:
        if not pk: 
            return Response({"detail": "Primary key is required"}, status=status.HTTP_400_BAD_REQUEST)

        #you can only edit your own expense:
        try:
            expense = Expense.objects.get(pk=pk, owner = request.user)
        except Expense.DoesNotExist:
            raise NotFound(detail="Task not found, or has other owner")
        
        #the actual editing: 
        serializer =  ExpensePostSerializer(expense, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: 
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        
        
    #DELETE: (overriding parent method to apply restrictions)
    @swagger_auto_schema(
            operation_description="Remove an expense."        
    )
    def destroy(self, *args, **kwargs):
        if self.request.user.is_staff: 
            return super().destroy(self.request,*args, **kwargs)
        else: 
            return Response("This action is not allowed for non-staff users", status=status.HTTP_403_FORBIDDEN)

