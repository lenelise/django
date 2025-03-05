'''
This is not in use anywhere (yet), just practicing for now. 
The idea was to retrict certain views according to the below access levels, but not sure if this
is a good use case for my models and applications as they are right now. I already customized a lot
overriding the get_queryset-methods and/or get_serializer_class-methods in the viewsets. 
'''

ACCESS_LEVEL_NAMES = [
    "none", 
    "superadmin",
    "administrator",
    "worker"
]

ACCESS_LEVELS = {
    "SUPERUSER": 1,
    "ADMINISTRATOR": 2,
    "WORKER": 3,
    "NONE": 0
}

ADMIN_ACCESS_LEVELS = [ACCESS_LEVELS['SUPERUSER'], ACCESS_LEVELS["ADMINISTRATOR"]]
EMPLOYEE_ACCESS_LEVELS = [ACCESS_LEVELS['WORKER']]

from rest_framework import permissions

def is_admin(user):
    return (user.access_level in ADMIN_ACCESS_LEVELS or user.is_superuser) and user.is_staff

def is_worker(user):
    return user.access_level in EMPLOYEE_ACCESS_LEVELS and user.is_staff

class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_admin(request.user)
    
class WorkerPermission(permissions.BasePermission):
    def has_permission(self,request,view):
        return is_worker(request.user)