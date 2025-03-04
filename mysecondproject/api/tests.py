from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from expensetracker.models import Expense, ExpenseCategory
from accounts.models import CustomUser

# Create your tests here.


# class ExpenseTestCase(APITestCase):
#     '''Test api/expenses'''

#     def setUp(self):
#         '''Create what is needed to run the tests:'''
#         self.admin_user = CustomUser.objects.create_superuser(username="superduper", password="Password321")
#         self.normal_user = CustomUser.objects.create_user(username='nonstaff3', password='password321')
#         self.expense_admin = Expense.objects.create(
#             title ="Admin Expense",
#             price = 100,
#             owner = self.admin_user
#         )
#         self.expense_normal = Expense.objects.create(
#             title = "Normal Expense",
#             price = 100,
#             owner = self.normal_user
#         )
#         self.url = reverse("expensetracker:expenses")

#     def test_get_expenses_admin(self):
#         '''Testing GET expenses for admin'''
#         self.client.login(username="superduper", password="Password321")
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Expense.objects.count(),2)

class ExpenseCategoryTestCase(APITestCase):
    '''Test api/categories'''

    def setUp(self):
        '''Create what is needed to run the tests:'''
        self.normal_user = CustomUser.objects.create_user(username='nonstaff3', password='password321')
        self.category = ExpenseCategory.objects.create(title="New category")
        self.url = reverse("categories")

    def test_get_categories(self):
        '''Testing GET categories'''
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        ''' Test creating new Category'''
        self.client.force_authenticate(user=self.normal_user)
        data = {"title": "New Category"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_categories_unauthorized(self):
        '''Testing to get the categories with un-authorized user'''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_categories_unauthorized(self):
        '''Testing to posta new category with un-authorized user'''
        data = {"title": "New Category"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)