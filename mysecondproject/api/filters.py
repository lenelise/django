import django_filters
from accounts.models import CustomUser

class CustomUserFilter(django_filters.FilterSet):
    class Meta: 
        model = CustomUser
        fields = {
            'username': ['exact'],
            # 'date_joined': ["month__gt"],
        }