from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User, Group
from rest_framework import permissions, status
from rest_framework.response import Response
from account.serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserActiveSerializer,
    UserDeleteSerializer,
    UserUpdateSerializer)
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)

class UserRegisterView(CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
        

class UserLoginView(APIView):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserActiveView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserActiveSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class UserDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserDeleteSerializer
    queryset = User.objects.all()
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class UserUpdateView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserUpdateSerializer
    def post(self,request):
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

