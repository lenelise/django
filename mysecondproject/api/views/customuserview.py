# from django.db.models import Q

# from rest_framework import viewsets,permissions, status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.exceptions import NotFound

# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

# from accounts.models import CustomUser
# from accounts.serializers import CustomUserSerializer, CustomUserPostSerializer

# class CustomUserView(APIView):

#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None) #if no pk is given it defaults to None

#         if pk: 
#             try:
#                 user = CustomUser.objects.get(pk=pk)
#             except CustomUser.DoesNotExist:
#                 raise NotFound(detail="Task not found, or has other owner")
#             serializer =  CustomUserSerializer(user, context={"request": request})
#         else: 
#             users = self.get_queryset()
#             serializer = CustomUserSerializer(users, many=True, context={"request": request})

#         return Response(serializer.data)   

