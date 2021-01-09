from datetime import tzinfo
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
from rest_framework.parsers import FileUploadParser
# Create your views here.
from record.serializers import *
import swagger
swagger_schema = swagger.SwaggerErrorSchema()


class TimeRecoringManualView(GenericAPIView):

    serializer_class = TimeRcordingManualSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Time.objects.all()
    @swagger_auto_schema(
        operation_description="date-time format: YYYY-MM-DD hh:mm:ss or iso-8601 (gregorian date)",
        responses={
            201: openapi.Response('Time Created' , TimeRcordingManualSerializer),
            400: openapi.Response('Bad Request',swagger_schema.get_schema('time-manual'))
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
        operation_description="date-time format: YYYY-MM-DD hh:mm:ss or iso-8601 (gregorian date)",
        responses={
            201: openapi.Response('Time Created' , TimeRcordingAutoSerializer),
            400: openapi.Response('Bad Request',swagger_schema.get_schema('time-auto'))
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
        operation_description="stop first incomplete time for user of passed token",
        responses={
            200: openapi.Response('Time Stopped' , TimeRecordingStopSerializer),
            400: openapi.Response('Bad Request',swagger_schema.get_schema('time-auto-stop'))
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
        operation_description="create new project (superuser access needed)",
        request_body=swagger.get_create_project_request_schema(),
        responses={
            201: openapi.Response('Project Created' , swagger.get_create_project_schema()),
            400: openapi.Response('Bad Request' , swagger_schema.get_schema('create-project'))
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
        operation_description="add a user to the project (superuser access needed)",
        responses={
            200: openapi.Response('User Added To Project' , AddUserToProjectSerializer),
            400: openapi.Response('Bad Request' , swagger_schema.get_schema('add-to-project'))
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
        operation_description="username=None returns all projects (superuser acccess needed) and username='user' returns user\'s projects \
                                     (user access and admin access) (gregorian date)",
        responses={
            200: openapi.Response('List Of Projects' , swagger.get_list_project_schema()),
            400: openapi.Response('Bad Request' , swagger_schema.get_schema('list-projects'))
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
                    print(pu.project.avatar=="")
                    project_list.append({
                        'name':pu.project.name,
                        'category':pu.project.category,
                        'start_time':str(tz.normalize(pu.project.start_time).replace(tzinfo=None)),
                        'end_time':str(tz.normalize(pu.project.end_time).replace(tzinfo=None)) if pu.project.end_time!=None else None,
                        'username':pu.user.username,
                        'avatar':pu.project.avatar.url if pu.project.avatar!="" else "",
                        'description': pu.project.description,
                        'budget':pu.project.budget
                    })
                return Response(project_list, status=status.HTTP_200_OK)
            else:
                project_list = list(Project.objects.all().values('name','category', 'start_time', 'end_time','avatar','description','budget'))
                for project in project_list:
                    
                    project['start_time'] = str(tz.normalize(project['start_time']).replace(tzinfo=None))
                    project['end_time'] = str(tz.normalize(project['end_time']).replace(tzinfo=None)) if project['end_time']!=None else None
                return Response((project_list), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListTimesView(GenericAPIView):

    serializer_class = ListTimesSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Time.objects.all()
    @swagger_auto_schema(
        operation_description="incomlete times not showing - gregorian date - 'duration' is in second - time zone (Asia/Tehran) - at least one filter needed",
        responses={
            200: openapi.Response('List Of Times' , swagger.get_list_time_schema()),
            400: openapi.Response('Bad Request' , swagger_schema.get_schema('list-times'))
        },
    )
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True): 
            username = request.data.get('username', None)
            project = request.data.get('project', None)
            start_time = request.data.get('start_time', None)
            end_time = request.data.get('end_time', None)

            tz = pytz.timezone("Asia/Tehran")
            times = None

            if username:
                times = Time.objects.filter(user__username=username)
            if project:
                if times != None:
                    times = times.filter(project__name=project)   
                else:
                    times = Time.objects.filter(project__name=project)
            if start_time:
                if times != None:
                    times = times.filter(start_time__gte=start_time)
                else:
                    times = Time.objects.filter(start_time__gte=start_time)
            
            if end_time:
                if times != None:
                    times = times.filter(end_time__lte=end_time)
                else:
                    times = Time.objects.filter(end_time__lte=end_time)
            times = times.filter(end_time__isnull=False)
            times = times.values("id","project","user","date","start_time","end_time","duration","description")
            times = list(times)
            
            for time in times:
                time['project'] = Project.objects.get(id=time['project']).name
                time['user'] = User.objects.get(id=time['user']).username
                time['start_time'] = tz.normalize(time['start_time'])
                time['date'] = str(time['date'])
                time['start_time'] = str(tz.normalize(time['start_time']).replace(tzinfo=None,microsecond=0))
                time['end_time'] = str(tz.normalize(time['end_time']).replace(tzinfo=None,microsecond=0)) if time['end_time']!=None else None
                time['duration'] = time['duration'].seconds if time['duration']!=None else None

            return Response(times, status=status.HTTP_200_OK)
           
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimeDeleteView(GenericAPIView):

    serializer_class = TimeDeleteSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Time.objects.all()
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Time Deleted' , TimeDeleteSerializer),
            400: openapi.Response('Bad Request' , swagger_schema.get_schema('delete-time'))
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
            200: openapi.Response("Time Updated", TimeUpdateSerializer),
            400: openapi.Response('Bad Request' , swagger_schema.get_schema('update-time'))
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
            400: openapi.Response("Bad Request", swagger_schema.get_schema('delete-project')),
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
            200: openapi.Response("Project update", swagger.get_update_project_schema()),
            400: openapi.Response("Bad Request", swagger_schema.get_schema('update-project')),
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
        operation_description="gregorian date - all information of specific project",
        responses={
            200: openapi.Response("Project update", swagger.get_datail_project_schema()),
            400: openapi.Response("Bad Request", swagger_schema.get_schema('detail-project')),
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            tz = pytz.timezone("Asia/Tehran")
            projects = Project.objects.filter(name=request.data.get('project',None)).values(
                'name', 'category', 'start_time', 'end_time','avatar','description', 'budget'
                )
            projects = list(projects)
            
            for project in projects:
                project['start_time'] = str(tz.normalize(project['start_time']).replace(microsecond=0,tzinfo=None))
                project['end_time'] = str(tz.normalize(project['end_time']).replace(microsecond=0,tzinfo=None)) if project['end_time']!=None else None
                
            return Response(projects, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




