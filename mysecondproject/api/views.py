from rest_framework import viewsets,permissions
from expensetracker.models import Expense
from expensetracker.serializers import ExpenseSerializer
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer

# Create your views here.

class ExpenseViewSet(viewsets.ModelViewSet):
    '''
        API endpoint to view or edit Expenses
    '''

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.AllowAny]
    #permission_classes = [permissions.IsAuthenticated]


class CustomUserViewSet(viewsets.ModelViewSet):
    '''
        API endpoint to view or edit users.
        Only allowed if you are authenticated as admin (staff). 
    '''

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    #permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAdminUser]
