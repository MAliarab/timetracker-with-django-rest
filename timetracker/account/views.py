from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.
import json
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from account.models import UserProfile
from record.models import ProjectUser
from rest_framework import permissions, status
from rest_framework.response import Response
from django.http import HttpResponse
from account.serializers import *
from rest_framework.views import APIView
from django.core import serializers
from rest_framework.generics import GenericAPIView
import swagger

swagger_schema = swagger.SwaggerErrorSchema()

class UserRegisterView(GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
        
    @swagger_auto_schema(
        operation_description="user activation after registration needed (/active-user)",

        responses={
            200: openapi.Response('register successfully.', swagger.get_registration_schema()),
            400: openapi.Response('Bad Request', swagger_schema.get_schema('register'))
        },
    )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(GenericAPIView):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_description="user login",

        responses={
            200: openapi.Response('login user successfully.', UserLoginSerializer),
            400: openapi.Response('Bad Request', swagger_schema.get_schema('login'))
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
        operation_description="user activation. (action=true) for activation (action=false) for deactivation",

        responses={
            200: openapi.Response('active user successfully.', UserActiveSerializer),
            400: openapi.Response('Bad Request', swagger_schema.get_schema('active-user'))
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
        operation_description="user delete",

        responses={
            200: openapi.Response('delete user successfully.', UserDeleteSerializer),
            400: openapi.Response('Bad Request', swagger_schema.get_schema('delete-user'))
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
        operation_description="user update",

        responses={
            200: openapi.Response('update user successfully.', UserUpdateSerializer),
            400: openapi.Response('Bad Request', swagger_schema.get_schema('update-user'))
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
        operation_description="list of users",

        responses={
            200: openapi.Response('update user successfully.', swagger.get_list_user_schema()),
            400: openapi.Response('Bad Request', swagger_schema.get_schema('list-users'))
        },
    )
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):

            project = request.data.get('project', None)
            is_working = request.data.get('is_working',None)
            user_profiles = None
            project_users = None
            users = User.objects.all()
            if project!=None:
                project_users = ProjectUser.objects.filter(project__name=project)
                users = users.filter(username__in=project_users.values('user__username'))
            if is_working!=None:
                user_profiles = UserProfile.objects.filter(is_working=is_working)
                users = users.filter(username__in=user_profiles.values('user__username'))
            users = users.values('username','first_name','last_name','is_active','is_superuser')
            users = list(users)
            for user in users:
                # userprofile = UserProfile.objects.filter(user__username=user['username'])  
                if user_profiles:
                    user['is_working'] = user_profiles.filter(user__username=user['username']).first().is_working
                if project_users:
                    # print(project_users.filter(user=user).first())
                    user['project'] = project_users.filter(user__username=user['username']).first().project.name
            return Response(users, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class UserDetailView(GenericAPIView):
    permissions_classes = [permissions.AllowAny]
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()  
    @swagger_auto_schema(
        operation_description="detail of user",

        responses={
            200: openapi.Response('update user successfully.', swagger.get_detail_user_schema()),
            400: openapi.Response('Bad Request', swagger_schema.get_schema('detail-users'))
        },
    )

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            users = User.objects.filter(username=request.data.get('username',None)).values(
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
                    user['job_type'] = userprofile.first().job_type
                    user['hours_per_month'] = userprofile.first().hours_per_month
            return Response(list(users), status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

