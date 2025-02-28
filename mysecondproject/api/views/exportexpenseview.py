# from rest_framework.views import APIView
# from rest_framework.permissions import IsAdminUser
# from .expenseviewset import ExpenseViewSet

# class ExportExpenseView(APIView):
#     permission_classes = [IsAdminUser]
    

#     queryset = ExpenseViewSet.get_queryset()

#     def get(self, request):
#         data = ExpenseViewSet.list(self, request)
#         return data
