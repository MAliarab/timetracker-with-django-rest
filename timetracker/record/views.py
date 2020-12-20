from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from record.models import Project, ProjectUser, Time
from django.contrib.auth.models import User
import jdatetime
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
    ProjectDeleteSerializer
)


class TimeRecoringManualView(APIView):

    serializer_class = TimeRcordingManualSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimeRecoringAutoView(APIView):

    serializer_class = TimeRcordingAutoSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimeRecoringStopView(APIView):

    serializer_class = TimeRecordingStopSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectCreateView(APIView):
    
    serializer_class = ProjectCreateSeralizer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AddUserToProjectView(APIView):

    
    serializer_class = AddUserToProjectSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListProjectView(APIView):

    serializer_class = ListProjectsSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = request.data.get('username', None)
            
            if username!=None:
                projectuser_list = ProjectUser.objects.filter(user__username=username)
                project_list = []
                
                for pu in projectuser_list:
                    
                    project_list.append({
                        'name':pu.project.name,
                        'category':pu.project.category,
                        'start_time':str(jdatetime.datetime.fromgregorian(datetime=pu.project.start_time)),
                        'end_time':str(jdatetime.datetime.fromgregorian(datetime=pu.project.end_time)) if pu.project.end_time!=None else None,
                        'username':pu.user.username
                    })
                return Response(project_list, status=status.HTTP_200_OK)
            else:
                project_list = list(Project.objects.all().values('name','category', 'start_time', 'end_time'))
                for project in project_list:
                    print(project)
                    project['start_time'] = str(jdatetime.datetime.fromgregorian(datetime=project['start_time']))
                    project['end_time'] = str(jdatetime.datetime.fromgregorian(datetime=project['end_time'])) if project['end_time']!=None else None
                return Response((project_list), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListTimesView(APIView):

    serializer_class = ListTimesSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = request.data.get('username', None)
            times = Time.objects.filter(user__username=username).values("id","project","user","date","start_time","end_time","duration","description")
            times = list(times)
            for time in times:
                time['project'] = Project.objects.get(id=time['project']).name
                time['user'] = User.objects.get(id=time['user']).username
                if time['duration']!=None:
                    time['duration'] = time['duration'].seconds
            return Response(times, status=status.HTTP_200_OK)

            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimeDeleteView(APIView):

    serializer_class = TimeDeleteSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimeUpdateView(APIView):

    serializer_class = TimeUpdateSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDeleteView(APIView):

    serializer_class = ProjectDeleteSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)