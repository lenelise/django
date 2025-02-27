from rest_framework import viewsets,permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from drf_yasg.utils import swagger_auto_schema

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer, CustomUserPostSerializer



class CustomUserViewSet(viewsets.ModelViewSet):
    '''
        API endpoint to view or edit users.
        Only allowed if you are authenticated as admin (staff). 
        Want: only admin with certain permission is allowed here. 
    '''

    # queryset = CustomUser.objects.all()
    # serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    #overriding get_queryset() since we want different behaviour depending on admin/non admin
    def get_queryset(self):
        if self.request.user.is_staff == True: 
            return CustomUser.objects.all()
        else: 
            return CustomUser.objects.filter(id=self.request.user.id)

    #overriding get_serializer_class since we have different serializers for GET and POST
    def get_serializer_class(self): 
        if self.action in ['create', 'update']: 
            return CustomUserPostSerializer
        else: 
            return CustomUserSerializer
        
    
    #GET: 
    def list(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None) #if no pk is given it defaults to None

        if pk: 
            try:
                user = CustomUser.objects.get(pk=pk)
            except CustomUser.DoesNotExist:
                raise NotFound(detail="Task not found, or has other owner")
            serializer =  CustomUserSerializer(user, context={"request": request})
        else: 
            users = self.get_queryset()
            serializer = CustomUserSerializer(users, many=True, context={"request": request})

        return Response(serializer.data)


    @swagger_auto_schema(
        operation_description="Create users. Only available for admin users."        
    )    
    def create(self, request, *args, **kwargs):
        serializer = CustomUserPostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
