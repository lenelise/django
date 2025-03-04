from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from expensetracker.models import Expense
from accounts.models import CustomUser

class ExpenseTestCase(APITestCase):
    '''Tests for GET api/expeses/'''

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
        self.detail_url = reverse('expense-detail', kwargs={'pk': self.expense_admin.pk})

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

    def test_get_expenses_unauthenticated(self):
        '''Unauthenticated GET expenses'''
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_expenses_normal(self):
        '''Authenticated POST api/expenses/ NON-ADMIN'''

        self.client.force_authenticate(user=self.normal_user)
        data = {
            "title": "New expense",
            "price": 100
        }
        response = self.client.post(self.list_url, data)
        # print(response.json())
        # print(Expense.objects.values())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.last().owner_id, self.normal_user.id) #checks owner is correctly assigned

    def test_delete_expense_normal(self):
        '''Authenticated DELETE api/expenses/ NON-ADMIN'''
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_expense_admin(self):
        '''Authenticated DELETE api/expenses/ ADMIN'''
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test PUT