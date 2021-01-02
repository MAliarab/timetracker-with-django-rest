from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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
    ListCreateAPIView,
    GenericAPIView
)

class UserRegisterView(CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
        
class UserLoginView(GenericAPIView):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        responses={
            200: openapi.Response('login successfully.', UserLoginSerializer),
            400: 'Bad Request'
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserActiveView(GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserActiveSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_description="use 'action=True' for activate and 'action=False' for deactivate",
        responses={
            200: openapi.Response('active/deactive successfully' , UserActiveSerializer),
            400: 'Bad Request'
        },
    )

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class UserDeleteView(GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserDeleteSerializer
    queryset = User.objects.all()
    @swagger_auto_schema(
        responses={
            200: openapi.Response('user delete successfully' , UserDeleteSerializer),
            400: 'Bad Request'
        },
    )

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class UserUpdateView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    @swagger_auto_schema(
        responses={
            200: openapi.Response('user update successfully' , UserUpdateSerializer),
            400: 'Bad Request'
        },
    )

    def post(self,request):
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class ListUsersView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ListUsersSerializer
    queryset = User.objects.all()
    @swagger_auto_schema(
        responses={
            200: openapi.Response('list of all users (superuser access needed)',
             examples=
             {
                "application/json":
                [
                    {
                        "username": "user",
                        "first_name": "firstname",
                        "last_name": "lastname",
                        "is_active": True,
                        "is_superuser": False,
                        "is_working": True
                    },
                ]
            }
                ),
            400: 'Bad Request'
        },
    )

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

class UserDetailView(GenericAPIView):
    permissions_classes = [permissions.AllowAny]
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()  
    @swagger_auto_schema(
        responses={
            200: openapi.Response('single user details',
             examples=
             {
                "application/json":
                [
                    {
                        "username": "user",
                        "first_name": "firstname",
                        "last_name": "lastname",
                        "is_active": True,
                        "is_superuser": False,
                        "is_working": True
                    },
                ]
            }
                ),
            400: 'Bad Request'
        },
    )

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

