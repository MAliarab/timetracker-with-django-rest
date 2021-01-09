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
            raise serializers.ValidationError("token is not valid")
        if project.exists():
            project_obj = project.first()
        else:
            raise serializers.ValidationError("project is not exist")
        
        if not ProjectUser.objects.filter(project=project_obj, user=token_obj.user).exists():
            raise serializers.ValidationError("user is not a member of the project")
        

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
        
        return data

class TimeRcordingAutoSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    project = serializers.CharField(
        required=True,
    )

    start_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        required=False,
        read_only=True
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
        date = datetime.datetime.now().date()
        start_time = datetime.datetime.now().replace(microsecond=0)
        

        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token is not valid")
        if project.exists():
            project_obj = project.first()
        else:
            raise serializers.ValidationError("project is not exist")
        
        if not ProjectUser.objects.filter(project=project_obj, user=token_obj.user).exists():
            raise serializers.ValidationError("this user is not a member of the project")
        
        times_list = Time.objects.filter(user=token_obj.user,end_time=None)
        if times_list.exists():
            time = times_list.first()
            raise serializers.ValidationError("you have an imcomplete time: "+str(time.start_time.astimezone(tz).replace(tzinfo=None)))

        try:
            Time.objects.create(
                project=project_obj,
                user=token_obj.user,
                date=(date),
                start_time=(start_time),
            )

            
        except Exception as e:
            raise serializers.ValidationError(e)
        
        data['start_time'] = start_time
        return data

class ProjectCreateSeralizer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    name = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Project.objects.all())]
    )

    category = serializers.CharField(
        required=True,

    )

    start_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        required=False,
        read_only=True
    )

    description = serializers.CharField(
        required=False,
    )

    budget = serializers.IntegerField(
        required=False,
        min_value=0
    )

    avatar = serializers.ImageField(
        required=False,

    )

    avatar_path = serializers.CharField(
        required=False,
        read_only=True
    )
    
    class Meta:
        model = Project
        fields = ['token', 'name', 'category','start_time', 'description', 'budget', 'avatar','avatar_path']
        write_only_fields = ('avatar',)
    
    def validate(self, data):

        token = Token.objects.filter(
            key= data.get('token', None)
            )

        data_cp = data.copy()
        del data_cp['token']

        tz = pytz.timezone('Asia/Tehran')
        start_time = datetime.datetime.now(tz).replace(microsecond=0)
        data_cp['start_time'] = start_time
        


        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token is not valid")
        
        if not token_obj.user.is_superuser:
            raise serializers.ValidationError("You have not access")
        
        try:
            p = Project.objects.create(**data_cp)
            if p.avatar:
                data['avatar_path'] = p.avatar.url
        except Exception as e:
            raise serializers.ValidationError(e)
        data['start_time'] = start_time
        if data.get('avatar',None):
            del data['avatar']
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
            raise serializers.ValidationError("You have not access")
        
        if user.exists():
            user_obj = user.first()
        else:
            raise serializers.ValidationError("user is not exist")

        if project.exists():
            project_obj = project.first()
        else:
            raise serializers.ValidationError("project is not exist")
        
        pu = ProjectUser.objects.filter(user=user_obj,project=project_obj)
        if pu.exists():
            raise serializers.ValidationError("user already added to this project")

        try:
            ProjectUser.objects.create(
                project=project_obj,
                user=user_obj
            )
        except Exception as e:
            raise serializers.ValidationError(e)


        return data

class ListProjectsSerializer(serializers.ModelSerializer):


    token = serializers.CharField(
        required=True,
    )

    username = serializers.CharField(
        required=False,
    )

    class Meta:
        model = Project
        fields = ('token','username')

    def validate(self,data):

        token = Token.objects.filter(key=data.get('token',None))
        username = data.get('username',None)
        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token is not valid")
        if (not token_obj.user.is_superuser) and (not token_obj.user.username==username):
            raise serializers.ValidationError("you have not access")
        
        return data

class TimeRecordingStopSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    description = serializers.CharField(
        required=True,
    )


    class Meta:
        model = Time
        fields = ['token', 'description']

    def validate(self, data):

        token = Token.objects.filter(key=data.get('token',None))
        description = data.get('description')
        tz = pytz.timezone("Asia/Tehran")
        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token is not valid")
        
        time = Time.objects.filter(user=token_obj.user, end_time=None)
        if time.exists():
            time_obj = time.first()
        else:
            raise serializers.ValidationError("there is no incomplete time for this user")
        try:
            now_time =  datetime.datetime.now()
            time_obj.end_time = now_time
            time_obj.duration = now_time - time_obj.start_time.astimezone(tz).replace(tzinfo=None)
            time_obj.description = description
            time_obj.save()
        except Exception as e:
            raise serializers.ValidationError(e)
        
        return data
        
class ListTimesSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    username = serializers.CharField(
        required=False,
    )

    project = serializers.CharField(
        required=False,
    )

    start_time = serializers.DateTimeField(
        required=False,
    )

    end_time = serializers.DateTimeField(
        required=False,
    )

    class Meta:
        model = Time
        fields = ['token', 'username', 'project', 'start_time', 'end_time']

    def validate(self, data):

        token = Token.objects.filter(key=data.get('token',None))
        username = data.get('username', None)
        project = data.get('project', None)
        start_time = data.get('start_time', None)
        end_time = data.get('end_time', None)
        
        if username:
            user = User.objects.filter(username=username)
        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token is not valid")
        if username:
            if (not token_obj.user.is_superuser) and (not token_obj.user.username==username):
                raise serializers.ValidationError("you have not access")
        else:
            if (not token_obj.user.is_superuser):
                raise serializers.ValidationError("you have not access")
        if username:
            if not user.exists():
                raise serializers.ValidationError("user is not exist")
        if all(v is None for v in [username, project, start_time, end_time]):
            raise serializers.ValidationError("must include at least one filter")
        return data   

class TimeDeleteSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    time_id = serializers.IntegerField(
        required=True,
    )

    class Meta:
        model = Time
        fields = ['token', 'time_id']

    def validate(self, data):

        token = Token.objects.filter(key=data.get('token',None))
        time_id = data.get('time_id', None)
        
        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token is not valid")
        
        time = Time.objects.filter(id=time_id)
        if time.exists():
            time_obj = time.first()
        else:
            raise serializers.ValidationError("time_id is not valid")
        
        if (not token_obj.user.is_superuser) and (not time_obj.user==token_obj.user):
            raise serializers.ValidationError("you have not access")

        try:
            time_obj.delete()

        except Exception as e:
            print(e)

        return data   

class TimeUpdateSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    time_id = serializers.IntegerField(
        required=True,
    )

    project = serializers.CharField(
        required=False,
    )

    start_time = serializers.DateTimeField(
        required=False,
    )

    end_time = serializers.DateTimeField(
        required=False,
    )

    description = serializers.CharField(
        required=False,
    )

    class Meta:
        model = Time
        fields = ['token','time_id', 'project', 'start_time', 'end_time', 'description']

    def validate(self,data):

        token = Token.objects.filter(key=data.get('token', None))
        time= Time.objects.filter(id=data.get('time_id',None))
        project = data.get('project')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        description = data.get('description')
        
        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token is not valid")
        
        if time.exists():
            time_obj = time.first()
        else:
            raise serializers.ValidationError("time_id is not valid")
        
        if (not token_obj.user.is_superuser) and (not token_obj.user==time_obj.user):
            raise serializers.ValidationError("you have not access")

        if project!=None:
            project_qs = Project.objects.filter(name=project)
            if project_qs.exists():
                project_obj = project_qs.first()
            else:
                raise serializers.ValidationError("project is not exist")
        
            project_user = None
            if token_obj.user.is_superuser:
                project_user = ProjectUser.objects.filter(project=project_obj)
            elif token_obj.user==time_obj.user:
                project_user = ProjectUser.objects.filter(project=project_obj,user=token_obj.user)
                print(project_user)
            if not project_user.exists():
                raise serializers.ValidationError("you are not member of project")
        

        if project:
            time_obj.project = project_obj
        
        if start_time:
            time_obj.start_time = start_time
        
        if end_time:
            time_obj.end_time = end_time
        
        if description:
            time_obj.description = description
        if time_obj.end_time:
            time_obj.duration = time_obj.end_time - time_obj.start_time

        try:
            time_obj.save()
        except Exception as e:
            print(e)

        return data
        
class ProjectDeleteSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    project = serializers.CharField(
        required=True,
    )

    class Meta:
        model = Project
        fields = ['token','project']

    def validate(self,data):

        token = Token.objects.filter(key=data.get('token',None))
        project = Project.objects.filter(name=data.get('project', None))

        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token is not valid")
        if not token_obj.user.is_superuser:
            raise serializers.ValidationError("you have not access")

        if project.exists():
            project_obj = project.first()
        else:
            raise serializers.ValidationError("project is not exist")

        try:
            project_obj.delete()
        except Exception as e:
            raise serializers.ValidationError(e)

        return data
    
class ProjectUpdateSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    project = serializers.CharField(
        required=True,
    )

    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Project.objects.all())],
        required=False,
    )

    category = serializers.CharField(
        required=False,
    )

    start_time = serializers.DateTimeField(
        required=False,
    )

    end_time = serializers.DateTimeField(
        required=False,
    )

    avatar = serializers.ImageField(
        required=False,
    )

    description = serializers.CharField(
        required=False,
    )

    budget = serializers.IntegerField(
        min_value=0,
        required=False,
    )
    
    avatar_path = serializers.CharField(
        read_only=True,
    )
        
    class Meta:
        model = Project
        fields = ['token','project','name','category','start_time','end_time','description','budget','avatar','avatar_path']

    def validate(self,data):

        token = Token.objects.filter(key=data.get('token',None))
        project = Project.objects.filter(name=data.get('project', None))
        new_project = data.get('new_project', None)
        data_cp = data.copy()
        del data_cp['token']
        if new_project:
            data_cp['name'] = new_project

        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token is not valid")
        
        if not token_obj.user.is_superuser:
            raise serializers.ValidationError("you have not access")

        if project.exists():
            project_obj = project.first()
        else:
            raise serializers.ValidationError("project is not exist")
        
        
        for (key,value) in data_cp.items():
            setattr(project_obj,key,value)

        try:
            project_obj.save()
        except Exception as e:
            raise serializers.ValidationError(e)
        if data.get('avatar',None):
            del data['avatar']
            data['avatar_path'] = project_obj.avatar.url
        return data
    
class ProjectDetailSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    project = serializers.CharField(
        required=True,
    )

    class Meta:
        model = Project
        fields = ['token','project']

    def validate(self,data):

        token = Token.objects.filter(key=data.get('token',None))
        project = Project.objects.filter(name=data.get('project', None))

        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token is not valid")
        if not token_obj.user.is_superuser:
            raise serializers.ValidationError("you have not access")

        if project.exists():
            project_obj = project.first()
        else:
            raise serializers.ValidationError("project is not exist")


        return data


