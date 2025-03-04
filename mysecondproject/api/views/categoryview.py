from django.db.models import Q

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from expensetracker.models import ExpenseCategory
from expensetracker.serializers import ExpenseCategorySerializer

class ExpenseCategoryView(APIView):
    #Everyone can see everything, so we dont need to override get_queryset
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Fetch all category data ." ) 
    def get(self, request): 
        categories = ExpenseCategory.objects.all()
        serializer = ExpenseCategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request): 
        serializer = ExpenseCategorySerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)