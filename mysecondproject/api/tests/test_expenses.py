from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from expensetracker.models import Expense
from accounts.models import CustomUser

class ExpenseTestCase(APITestCase):
    '''Tests for authenticated use of Expense APIs'''

    def setUp(self):
        '''Create what is needed to run the tests:'''
        self.admin_user = CustomUser.objects.create_superuser(username="superduper", password="Password321")
        self.normal_user = CustomUser.objects.create_user(username='nonstaff3', password='password321')
        self.expense_admin = Expense.objects.create(
            title ="Admin Expense",
            price = 100,
            owner = self.admin_user
        )
        self.expense_normal = Expense.objects.create(
            title = "Normal Expense",
            price = 100,
            owner = self.normal_user
        )
        self.list_url = reverse("expense-list")
        # self.create_url = reverse("expense-create")

    def test_get_expenses_admin(self):
        '''Authenticated GET expenses ADMIN'''
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Expense.objects.count(),2)

    def test_get_expenses_normal(self):
        '''Authenticated GET expenses NON-ADMIN'''
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()),1)

    def test_get_expenses_unauthicated(self):
        '''Unauthenticated GET expenses'''
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



