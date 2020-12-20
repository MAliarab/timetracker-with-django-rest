from django.shortcuts import render

# Create your views here.
import json
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from account.models import UserProfile
from rest_framework import permissions, status
from rest_framework.response import Response
from django.http import HttpResponse
from account.serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserActiveSerializer,
    UserDeleteSerializer,
    UserUpdateSerializer,
    ListUsersSerializer,
    UserDetailSerializer)
from rest_framework.views import APIView
from django.core import serializers
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    ListAPIView,
    RetrieveAPIView,
    ListCreateAPIView
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

class ListUsersView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ListUsersSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            users = User.objects.filter(is_staff=False).values('username','first_name','last_name','is_active','is_superuser')
            users_list = list(users)

            for user in users_list:
                userprofile = UserProfile.objects.filter(user__username=user['username'])
                
                if userprofile.exists():
                    user['is_working'] = userprofile.first().is_working
            return Response(list(users), status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class UserDetailView(APIView):
    permissions_classes = [permissions.AllowAny]
    serializer_class = UserDetailSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            users = User.objects.filter(is_staff=False,username=request.data.get('username',None)).values(
                'username',
                'first_name',
                'last_name',
                'is_active',
                'is_superuser',
            )
            users_list = list(users)
            for user in users_list:
                userprofile = UserProfile.objects.filter(user__username=user['username'])  
                if userprofile.exists():
                    user['is_working'] = userprofile.first().is_working
            return Response(list(users), status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

