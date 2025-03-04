from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from expensetracker.models import ExpenseCategory
from accounts.models import CustomUser

class ExpenseCategoryTestCase(APITestCase):
    '''Tests for authenticated and unauthenticated use of Category-APIs.'''

    def setUp(self):
        self.normal_user = CustomUser.objects.create_user(username='nonstaff3', password='password321')
        self.category = ExpenseCategory.objects.create(title="New category")
        self.url = reverse("categories")

    def test_get_categories(self):
        '''Authenticated GET api/categories/'''
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        '''Authenticated POST api/categories/'''
        self.client.force_authenticate(user=self.normal_user)
        data = {"title": "New Category"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_categories_unauthorized(self):
        '''Unauthenticated GET api/categories/'''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_categories_unauthorized(self):
        '''Unauthenticated POST api/categories/'''
        data = {"title": "New Category"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)