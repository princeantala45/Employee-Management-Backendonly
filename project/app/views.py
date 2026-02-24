from typing import cast
from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from .serializers import *
def index(request):
    return render(request,"index.html")

@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    return Response(
        {'message': 'Invalid credentials'},
        status=status.HTTP_400_BAD_REQUEST
    )
        
class RegisterUser(APIView):
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = cast(User, serializer.save())

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
        
    
class EmployeeRoleViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = EmployeeRole.objects.all()
    serializer_class = EmployeeRoleSerializers
    
    def perform_create(self, serializer):        
        serializer.save(user=self.request.user)
        
class EmployeeLeaveViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = EmployeeLeave.objects.all()
    serializer_class = EmployeeLeaveSerializers
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class EmployeeSalaryViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = EmployeeSalary.objects.all()
    serializer_class = EmployeeSalarySerializers
    
class EmployeeAttandenceViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = EmployeeAttandence.objects.all()
    serializer_class = EmployeeAttandenceSerializers