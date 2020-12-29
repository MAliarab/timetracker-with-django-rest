from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from record.models import Project, ProjectUser, Time
from django.contrib.auth.models import User
import jdatetime
import pytz
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.
from record.serializers import (
    TimeRcordingManualSerializer,
    ProjectCreateSeralizer,
    AddUserToProjectSerializer,
    TimeRcordingAutoSerializer,
    ListProjectsSerializer,
    TimeRecordingStopSerializer,
    ListTimesSerializer,
    TimeDeleteSerializer,
    TimeUpdateSerializer,
    ProjectDeleteSerializer,
    ProjectUpdateSerializer,
    ProjectDetailSerializer
)


class TimeRecoringManualView(GenericAPIView):

    serializer_class = TimeRcordingManualSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Time.objects.all()
    @swagger_auto_schema(
        operation_description="date-time format: YYYY-MM-DD hh:mm:ss (gregorian date)",
        responses={
            201: openapi.Response('manual time recording' , TimeRcordingManualSerializer),
            400: 'Bad Request'
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimeRecoringAutoView(GenericAPIView):

    serializer_class = TimeRcordingAutoSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Time.objects.all()
    @swagger_auto_schema(
        responses={
            201: openapi.Response('auto time recording' , TimeRcordingAutoSerializer),
            400: openapi.Response('auto time recording' , 
                examples= {
                    "application/json":
                        {
                            "non_field_errors": [
                                "project does not exist"
                            ]
                        }
                }
            )
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimeRecoringStopView(GenericAPIView):

    serializer_class = TimeRecordingStopSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Time.objects.all()
    @swagger_auto_schema(
        responses={
            200: openapi.Response('stop auto time recording' , TimeRecordingStopSerializer),
            400: 'Bad Request'
        },
    )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectCreateView(GenericAPIView):
    
    serializer_class = ProjectCreateSeralizer
    permission_classes = [permissions.AllowAny]
    queryset = Project.objects.all()
    @swagger_auto_schema(
        operation_description="superuser access needed",
        responses={
            201: openapi.Response('create new project' , ProjectCreateSeralizer),
            400: 'Bad Request'
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddUserToProjectView(GenericAPIView):

    serializer_class = AddUserToProjectSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Project.objects.all()
    @swagger_auto_schema(
        operation_description="superuser access needed",
        responses={
            201: openapi.Response('add a user to project' , AddUserToProjectSerializer),
            400: 'Bad Request'
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListProjectView(GenericAPIView):

    serializer_class = ListProjectsSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Project.objects.all()
    @swagger_auto_schema(
        operation_description="username=None returns all projects (admin acccess) and username='user' returns user\'s projects (user access and admin acccess)\
                                    (jalali date)",
        responses={
            200: openapi.Response("list of projects",
             examples=
             {
                "application/json":
                [
                    {
                        "name": "p11",
                        "category": "ai",
                        "start_time": "1399-09-23 14:09:23.107449+0000",
                        "end_time": "1399-09-30 08:22:00+0000",
                        "username": "m"
                    },
                ]
            }
                ),
            400: 'Bad Request'
        },
    )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = request.data.get('username', None)
            tz = pytz.timezone("Asia/Tehran")
            if username!=None:
                projectuser_list = ProjectUser.objects.filter(user__username=username)
                project_list = []
                
                for pu in projectuser_list:
                    
                    project_list.append({
                        'name':pu.project.name,
                        'category':pu.project.category,
                        'start_time':str(jdatetime.datetime.fromgregorian(datetime=tz.normalize(pu.project.start_time))),
                        'end_time':str(jdatetime.datetime.fromgregorian(datetime=tz.normalize(pu.project.end_time))) if pu.project.end_time!=None else None,
                        'username':pu.user.username
                    })
                return Response(project_list, status=status.HTTP_200_OK)
            else:
                project_list = list(Project.objects.all().values('name','category', 'start_time', 'end_time'))
                for project in project_list:
                    
                    project['start_time'] = str(jdatetime.datetime.fromgregorian(datetime=tz.normalize(project['start_time'])))
                    project['end_time'] = str(jdatetime.datetime.fromgregorian(datetime=tz.normalize(project['end_time']))) if project['end_time']!=None else None
                return Response((project_list), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListTimesView(GenericAPIView):

    serializer_class = ListTimesSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Time.objects.all()
    @swagger_auto_schema(
        operation_description="jalali date - 'duration' is in second - time zone (Asia/Tehran)",
        responses={
            200: openapi.Response("list of projects",
             examples=
             {
                "application/json":
                [
                    {
                      "id": 30,
                      "project": 10,
                      "user": 12,
                      "date": "1399-10-07",
                      "start_time": "1399-10-07 19:19:33+0330",
                      "end_time": "1399-10-07 19:21:41+0330",
                      "duration": 128,
                      "description": "this is..."
                    },
                    
                ]
            }
                ),
            400: 'Bad Request'
        },
    )
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            tz = pytz.timezone("Asia/Tehran")
            username = request.data.get('username', None)
            times = Time.objects.filter(user__username=username).values("id","project","user","date","start_time","end_time","duration","description")
            times = list(times)
            for time in times:
                time['project'] = Project.objects.get(id=time['project']).name
                time['user'] = User.objects.get(id=time['user']).username
                time['start_time'] = tz.normalize(time['start_time'])
                if time['end_time']!=None:
                    time['end_time'] = tz.normalize(time['end_time'])
                time['date'] = str(jdatetime.date.fromgregorian(date=time['date']))
                time['start_time'] = str(jdatetime.datetime.fromgregorian(datetime=time['start_time'].replace(microsecond=0)))
                time['end_time'] = str(jdatetime.datetime.fromgregorian(datetime=time['end_time'].replace(microsecond=0))) if time['end_time']!=None else None
                if time['duration']!=None:
                    time['duration'] = time['duration'].seconds
            return Response(times, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimeDeleteView(GenericAPIView):

    serializer_class = TimeDeleteSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Time.objects.all()
    @swagger_auto_schema(
        responses={
            200: openapi.Response("Time delete", TimeDeleteSerializer),
            400: 'Bad Request'
        },
    )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimeUpdateView(GenericAPIView):

    serializer_class = TimeUpdateSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Time.objects.all()
    @swagger_auto_schema(
        responses={
            200: openapi.Response("Time update", TimeUpdateSerializer),
            400: 'Bad Request'
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDeleteView(GenericAPIView):

    serializer_class = ProjectDeleteSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Project.objects.all()
    @swagger_auto_schema(
        responses={
            200: openapi.Response("Project delete", ProjectDeleteSerializer),
            400: 'Bad Request'
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProjectUpdateView(GenericAPIView):

    serializer_class = ProjectUpdateSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Project.objects.all()
    @swagger_auto_schema(
        responses={
            200: openapi.Response("Project update", ProjectUpdateSerializer),
            400: 'Bad Request'
        },
    )
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetailView(GenericAPIView):

    serializer_class = ProjectDetailSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Project.objects.all()
    @swagger_auto_schema(
        responses={
            200: openapi.Response("Project detail",
                examples={
                    "application/json":
                    [

                        {
                            "name": "p11",
                            "category": "ai",
                            "start_time": "1399-09-23 14:09:23+0000",
                            "end_time": "1399-09-30 08:22:00+0000"
                        }
                    ]
                }
            ),
            400: 'Bad Request'
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            tz = pytz.timezone("Asia/Tehran")
            projects = Project.objects.filter(name=request.data.get('project',None)).values('name', 'category', 'start_time', 'end_time')
            projects = list(projects)
            
            for project in projects:
                print(str(jdatetime.datetime.fromgregorian(datetime=tz.normalize(project['start_time']))))
                project['start_time'] = str(jdatetime.datetime.fromgregorian(datetime=project['start_time'].replace(microsecond=0)))
                project['end_time'] = str(jdatetime.datetime.fromgregorian(datetime=project['end_time'].replace(microsecond=0))) if project['end_time']!=None else None
                
            return Response(projects, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 