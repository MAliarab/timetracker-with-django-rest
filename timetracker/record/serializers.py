from rest_framework import serializers
from record.models import Time, Project, ProjectUser
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
import datetime, pytz, jdatetime

class TimeRcordingManualSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    project = serializers.CharField(
        required=True,
    )

    # user = serializers.CharField(
    #     required=True,
    # )

    start_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        required=True,
        )

    end_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        required=True,
        )

    description = serializers.CharField(
        required=True,
    )

    
    class Meta:
        model = Time
        fields = ['token', 'project', 'start_time', 'end_time','description']

    
    def validate(self, data):

        token = Token.objects.filter(
            key= data.get('token', None)
            )
        project = Project.objects.filter(
            name=data.get('project', None)
        )

        
        start_time = data.get('start_time', None)
        end_time = data.get('end_time', None)
        description = data.get('description', None)
        duration = end_time - start_time
        tz = pytz.timezone('Asia/Tehran')
        date = datetime.datetime.now(tz).date()

        
        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token in not valid")
        if project.exists():
            project_obj = project.first()
        else:
            raise serializers.ValidationError("project is not exist")
        
        # if token_obj.user.exists():
        #     raise serializers.ValidationError("user is not exist")
        
        if not ProjectUser.objects.filter(project=project_obj, user=token_obj.user).exists():
            raise serializers.ValidationError("this user is not a member of the project")
        

        try:
            Time.objects.create(
                project=project_obj,
                user=token_obj.user,
                date=(date),
                start_time=(start_time),
                end_time=(end_time),
                duration=duration,
                description=description
            )
        except Exception as e:
            raise serializers.ValidationError(e)
        
        data['start_time'] = jdatetime.datetime.fromgregorian(datetime=start_time)
        data['end_time'] = jdatetime.datetime.fromgregorian(datetime=end_time)
        return data

class TimeRcordingAutoSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    project = serializers.CharField(
        required=True,
    )

    start_time = serializers.DateTimeField(
        required=False,
    )
    
    class Meta:
        model = Time
        fields = ['token', 'project','start_time']

    
    def validate(self, data):

        token = Token.objects.filter(
            key= data.get('token', None)
            )
        project = Project.objects.filter(
            name=data.get('project', None)
        )

        tz = pytz.timezone('Asia/Tehran')
        date = datetime.datetime.now(tz).date()
        start_time = datetime.datetime.now(tz)
        
        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token in not valid")
        if project.exists():
            project_obj = project.first()
        else:
            raise serializers.ValidationError("project is not exist")
        
        # if token_obj.user.exists():
        #     raise serializers.ValidationError("user is not exist")
        
        if not ProjectUser.objects.filter(project=project_obj, user=token_obj.user).exists():
            raise serializers.ValidationError("this user is not a member of the project")
        
        
        try:
            Time.objects.create(
                project=project_obj,
                user=token_obj.user,
                date=(date),
                start_time=(start_time),
            )

            
        except Exception as e:
            raise serializers.ValidationError(e)
        
        data['start_time'] = jdatetime.datetime.fromgregorian(datetime=start_time)
        return data


class ProjectCreateSeralizer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    name = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Project.objects.all(), message="project already exists")]
    )

    category = serializers.CharField(
        required=True,

    )

    start_time = serializers.DateTimeField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = Project
        fields = ['token', 'name', 'category','start_time']

    
    def validate(self, data):

        token = Token.objects.filter(
            key= data.get('token', None)
            )
        name = data.get('name', None)
        category = data.get('category', None)
        tz = pytz.timezone('Asia/Tehran')
        start_time = datetime.datetime.now(tz)

        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token is not valid")
        
        user = User.objects.filter(
            username=token_obj.user
        )

        if user.exists():
            user_obj = user.first()
        else:
            raise serializers.ValidationError("user is not exist")

        if not user_obj.is_superuser:
            raise serializers.ValidationError("You have not admin access")
        
        try:
            Project.objects.create(
                name=name,
                category=category,
                start_time=str(start_time)
                      
            )
        except Exception as e:
            print('db error')
            raise serializers.ValidationError(e)
        data['start_time'] = jdatetime.datetime.fromgregorian(datetime=start_time)
        
        return data


class AddUserToProjectSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    username = serializers.CharField(
        required=True,
    )

    project_name = serializers.CharField(
        required=True,

    )

    class Meta:
        model = ProjectUser
        fields = ['token', 'username', 'project_name']

    
    def validate(self, data):

        token = Token.objects.filter(
            key= data.get('token', None)
            )

        user = User.objects.filter(
            username=data.get('username', None)
            )

        project = Project.objects.filter(
            name=data.get('project_name', None)
            )

        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token is not valid")
        
        if not token_obj.user.is_superuser:
            raise serializers.ValidationError("You have not admin access")
        
        if user.exists():
            user_obj = user.first()
        else:
            raise serializers.ValidationError("user is not exist")

        if project.exists():
            project_obj = project.first()
        else:
            raise serializers.ValidationError("project is not exists")

        try:
            ProjectUser.objects.create(
                project=project_obj,
                user=user_obj
            )
        except Exception as e:
            raise serializers.ValidationError(e)


        return data

