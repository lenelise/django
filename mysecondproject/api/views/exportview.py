from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from expensetracker.serializers import ExpenseGetSerializer
from accounts.serializers import CustomUserSerializer
from .expenseviewset import ExpenseViewSet

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from expensetracker.models import Expense
from accounts.models import CustomUser

import csv

class ExportView(APIView):
    permission_classes = [IsAdminUser] 
    # authentication_classes = [JWTAuthentication] #to force JWT for this endpoint

    def get(self, request):
        type = request.query_params.get("type") #expense eller user

        if type == "expenses": 
            return self.export_expenses(request)
        elif type == "users": 
            return self.export_users(request)
        else: 
            return Response({"error": "Ugyldig type."}) #bør kanskje raise proper expections/response code. gir 200 nå
        
    def export_expenses(self, request):
        expenses = Expense.objects.all()
        serializer = ExpenseGetSerializer(expenses, many=True,context={'request': request})
        
        response = HttpResponse(content_type="text/csv") #tells the browser that the reponse is a csv, not html or json
        response["Content-Disposition"] = 'attachment; filename="expenses.csv"' #tells the browser that it should download a file, not display a page

        fieldnames = ["url", "title", "content", "price", "date", "owner"]
        
        return self.write_to_csv(
            fieldnames=fieldnames, 
            data = serializer.data, 
            response = response)

        
    def export_users(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True,context={'request': request})
        
        response = HttpResponse(content_type="text/csv") #tells the browser that the reponse is a csv, not html or json
        response["Content-Disposition"] = 'attachment; filename="users.csv"' #tells the browser that it should download a file, not display a page

        fieldnames = ['username', 'date_of_birth']
        
        return self.write_to_csv(
            fieldnames=fieldnames, 
            data = serializer.data, 
            response = response)
    
    def write_to_csv(self, fieldnames, data, response):
        '''
            method to write the actual csv of the export
        '''
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        for row in data: 
            cleaned_row = {}
            for field in fieldnames: 
                cleaned_row[field] = row.get(field, "")
            writer.writerow(cleaned_row)
        return response
        
        