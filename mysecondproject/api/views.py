from rest_framework import viewsets,permissions, status
from rest_framework.response import Response
from expensetracker.models import Expense
from expensetracker.serializers import ExpenseSerializer
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    '''
        GET: non staff users can see own expenses, admin users can see all. 
        POST: same behavior for all, you can only add expenses to yourself. 
        PUT: non staff users can edit own expenses, admins can edit all. 
        DELETE: non admin user cannot delete expenses, admin users can delete any expense. 
    '''
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Expense.objects.all()  #a reference point, will be edited in method get_queryset() below

    # overriding parent get_queryset method
    def get_queryset(self):
        '''
        returns an iterable of objects from the database
        provides the data that will be used in POST, GET, PUT and DELTE 
        '''
        if self.request.user.is_staff == False:
            return Expense.objects.filter(owner=self.request.user)
        else: 
            return Expense.objects.all()
    
    #GET (overriding parent method to apply restrictions)
    #def list(request, *args, **kwargs)


    #POST: (overriding parent method to apply restrictions)
    def create(self, request, *args, **kwargs):
        serializer = ExpenseSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #PUT: (overriding parent method to apply restrictions)
    #def update(request, *args, **kwargs):
        
    
    #DELETE: (overriding parent method to apply restrictions)
    def destroy(self, *args, **kwargs):
        if self.request.user.is_staff: 
            return super().destroy(self.request,*args, **kwargs)
        else: 
            return Response("This action is not allowed for non-staff users", status=status.HTTP_403_FORBIDDEN)

class CustomUserViewSet(viewsets.ModelViewSet):
    '''
        API endpoint to view or edit users.
        Only allowed if you are authenticated as admin (staff). 
        Want: only admin with certain permission is allowed here. 
    '''

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]
