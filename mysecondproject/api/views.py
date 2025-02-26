from rest_framework import viewsets,permissions, status
from rest_framework.response import Response
from expensetracker.models import Expense
from expensetracker.serializers import ExpenseSerializer
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    '''
        API endpoint to view or edit Expenses. 
        Admin users can see all expenses. 
        Non-admin users can see their own expenses. 
    '''
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = Expense.objects.all()  #a reference point, will be edited in method get_queryset() below

    def get_queryset(self):
        '''
            Overriding get_queryset from ModelViewSet to apply restrictions for non-admin users. 
        '''
        if self.request.user.is_staff == False:
            return Expense.objects.filter(owner=self.request.user)
        else: 
            return Expense.objects.all()
        
    def destroy(self, *args, **kwargs):
        '''
            Override destroy from ModelViewSet to apply restrictions. Only admin users should be able to DELETE expenses.
        '''
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
