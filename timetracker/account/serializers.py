from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db.models import Q
from rest_framework.authtoken.models import Token
from account.models import UserProfile
from django.contrib.auth.hashers import mask_hash, make_password
from account.models import UserProfile

class UserRegisterSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    first_name = serializers.CharField(
        required=True,
    )

    last_name = serializers.CharField(
        required=True,
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        min_length=8,style={'input_type':'password'}
    )

    job_type = serializers.CharField(
        required=True
    )

    hours_per_month = serializers.FloatField(
        required=False,
    )

    class Meta:
        model = User
        fields = ('id',  'username', 'first_name', 'last_name', 'email', 'password','job_type', 'hours_per_month')

    def validate(self, data):
        try:
            user = User.objects.create_user(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=(data['password']),
                is_active=False,
                )
            user_profile = UserProfile.objects.filter(user=user)
            if user_profile.exists():
                user_profile_obj = user_profile.first()
                user_profile_obj.job_type = data['job_type']
                user_profile_obj.hours_per_month = data['hours_per_month']
                user_profile_obj.save()
            
        except Exception as e:
            raise Exception("database error")
        return data

    

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required = True,
    )

    token = serializers.CharField(
        allow_blank=True,
        read_only=True
    )

    password = serializers.CharField(
        required = True,
        style={'input_type':'password'}
    )

    class Meta:
        model = User
        fields = ('username','password','token')

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        
        user = User.objects.filter(
            Q(username=username)
        )
        if user.exists():
            user_obj = user.first()
        else:
            raise serializers.ValidationError("username in not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("password in not correct")
            if not user_obj.is_active:
                raise serializers.ValidationError("user is not active")
            else:
                token, created = Token.objects.get_or_create(user=user_obj)
                data['token'] = token.key
                data['password'] = make_password(password)
                
        else:
            raise serializers.ValidationError("user is not exists")
        
        return data

class UserActiveSerializer(serializers.ModelSerializer):
    
    token = serializers.CharField(
        required=True,
    )

    username = serializers.CharField(
        required=True,
    )

    # set action True for activate and set it False for dectivate user
    action = serializers.BooleanField(
        required=True
    )

    class Meta:
        model=Token
        fields = ('token','username','action')

    def validate(self, data):

        token = Token.objects.filter(key=data['token'])
        user = User.objects.filter(username=data['username'])
        action = data.get('action',None) #True for activate False for dectivate
        if action==None:
            raise serializers.ValidationError('action is None')
        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token in not valid")
        if not token_obj.user.is_superuser:
            raise serializers.ValidationError("you have not admin access") 
        if user.exists():
            user_obj = user.first()
        else:
            raise serializers.ValidationError("username in not valid")
        if action:
            user_obj.is_active = True
        else:
            user_obj.is_active = False
        try:
            user_obj.save()
        except:
            raise serializers.ValidationError("databse error")
        return data

class UserDeleteSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    username = serializers.CharField(
        required=True,
    )

    class Meta:
        model = Token
        fields = ('token','username')

    def validate(self, data):

        token = Token.objects.filter(key=data.get('token',None))
        user = User.objects.filter(username=data.get('username',None))
        
        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token in not valid")
        if not token_obj.user.is_superuser:
            raise serializers.ValidationError("you have not admin access") 
        if user.exists():
            user_obj = user.first()
        else:
            raise serializers.ValidationError("username in not valid")
        
        try:
            user_obj.delete()
        except Exception as e:
            raise serializers.ValidationError(e)
        return data

class UserUpdateSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    username = serializers.CharField(
        required=True,
    )

    first_name = serializers.CharField(
        required=False,
    )

    last_name = serializers.CharField(
        required=False,
    )

    email = serializers.EmailField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        required=False,
        min_length=8,style={'input_type':'password'}
    )
    

    class Meta:
        model = User
        fields = ('token','username','first_name', 'last_name', 'email', 'password')

    def validate(self, data):

        token = Token.objects.filter(key=data['token'])
        user = User.objects.filter(username=data['username'])
        username = data.get('username',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        email = data.get('email',None)
        password = data.get('password',None)


        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token in not valid")
        if (not token_obj.user.is_superuser) and (not token_obj.user.username==username):
            raise serializers.ValidationError("you have not access to this action")

        if user.exists():
            user_obj = user.first()
        else:
            raise serializers.ValidationError("username in not valid")
        
        if first_name:
            user_obj.first_name = first_name
        if last_name:
            user_obj.last_name = last_name
        if email:
            user_obj.email = email
        if password:
            user_obj.password = password

        try:
            user_obj.save()
        except Exception as e:
            raise serializers.ValidationError(e)
        new_data = user_obj.__dict__
        new_data['token'] = token_obj.key
        return new_data

class ListUsersSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )
    
    project = serializers.CharField(
        required=False,
    )

    is_working = serializers.BooleanField(
        required=False,
    )

    
    class Meta:
        model = User
        fields = ['token','project','is_working']
        

    def validate(self,data):

        token = Token.objects.filter(key=data.get('token',None))

        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token is not valid")
        if not token_obj.user.is_superuser:
            raise serializers.ValidationError("you have not admin access")
        
        return data

class UserDetailSerializer(serializers.ModelSerializer):

    token = serializers.CharField(
        required=True,
    )

    username = serializers.CharField(
        required=True,
    )

    class Meta:
        model = User
        fields = ['token','username']

    def validate(self,data):

        token = Token.objects.filter(key=data.get('token',None))
        username = data.get('username', None)
        if token.exists():
            token_obj = token.first()
        else:
            raise serializers.ValidationError("token is not valid")
        if (not token_obj.user.is_superuser) and (not token_obj.user.username==username):

            raise serializers.ValidationError("you have not access to this action")
        
        return data

