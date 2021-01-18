from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.settings import api_settings

from drf_yasg.errors import SwaggerValidationError

def get_list_user_schema():
    return openapi.Schema(
        "List Of Users",
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING,title='Username'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING,title='First name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING,title='Last name'),
                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN,title='User activation status'),
                'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN,title='Superuser access'),
                'is_working': openapi.Schema(type=openapi.TYPE_BOOLEAN,title='User working status'),
                'project': openapi.Schema(type=openapi.TYPE_STRING,title='Project name'),
            },
            required=['username', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_working']
        )
    )

def get_detail_user_schema():
    return openapi.Schema(
        "Detail Of User",
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING,title='Username'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING,title='First name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING,title='Last name'),
                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN,title='User activation status'),
                'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN,title='Superuser access'),
                'is_working': openapi.Schema(type=openapi.TYPE_BOOLEAN,title='User working status'),
                'job_type': openapi.Schema(type=openapi.TYPE_STRING,title='Job type'),
                'hours_per_month': openapi.Schema(type=openapi.TYPE_STRING,title='Monthly commitment'),
                'avatar': openapi.Schema(type=openapi.TYPE_STRING,title='Avatar'),
            },
            required=['username', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_working','job_type','hours_per_month','avatar']
        )
    )

def get_create_project_request_schema():
    return openapi.Schema(
        "Create Project",
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING,title='Project name'),
            'category': openapi.Schema(type=openapi.TYPE_STRING,title='Project category'),
            'description': openapi.Schema(type=openapi.TYPE_STRING,title='Description'),
            'end_time': openapi.Schema(type=openapi.TYPE_STRING,title='End time'),
            'budget': openapi.Schema(type=openapi.TYPE_INTEGER,title='Budget'),
            'avatar': openapi.Schema(type=openapi.TYPE_FILE,title='Avatar (Image file)'),
        },
        required=['name', 'category']
    )

def get_create_project_schema():
    return openapi.Schema(
        "Create Project",
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING,title='Project name'),
            'category': openapi.Schema(type=openapi.TYPE_STRING,title='Project category'),
            'start_time': openapi.Schema(type=openapi.TYPE_STRING,title='Start time'),
            'end_time': openapi.Schema(type=openapi.TYPE_STRING,title='End time'),
            'description': openapi.Schema(type=openapi.TYPE_STRING,title='Description'),
            'budget': openapi.Schema(type=openapi.TYPE_INTEGER,title='Budget'),
            'avatar_path': openapi.Schema(type=openapi.TYPE_STRING,title='Avatar path'),
        },
        required=['name', 'category','start_time']
    )

def get_registration_schema():
    return openapi.Schema(
        "User Register",
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING,title='Username'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING,title='First name'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING,title='Last name'),
            'email': openapi.Schema(type=openapi.TYPE_STRING,title='Email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING,title='Password'),
            'job_type': openapi.Schema(type=openapi.TYPE_STRING,title='Job type'),
            'hours_per_month': openapi.Schema(type=openapi.TYPE_NUMBER,title='Monthly commitment'),
        },
        required=['username', 'first_name', 'last_name', 'email', 'password', 'job_type', 'hours_per_month']
    )

def get_list_project_schema():
    return openapi.Schema(
        "List Of Projects",
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING,title='Username'),
                'name': openapi.Schema(type=openapi.TYPE_STRING,title='Project name'),
                'category': openapi.Schema(type=openapi.TYPE_STRING,title='Category'),
                'start_time': openapi.Schema(type=openapi.TYPE_STRING,title='Start time'),
                'end_time': openapi.Schema(type=openapi.TYPE_STRING,title='End time'),
                'avatar': openapi.Schema(type=openapi.TYPE_STRING,title='Path of avatar'),
                'description': openapi.Schema(type=openapi.TYPE_STRING,title='Description'),
                'budget': openapi.Schema(type=openapi.TYPE_NUMBER,title='Project name'),
            },
            required=['name', 'category', 'start_time', 'end_time', 'avatar', 'description', 'budget']
        )
    )


def get_list_time_schema():
    return openapi.Schema(
        "List Of Projects",
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING,title='Time id'),
                'project': openapi.Schema(type=openapi.TYPE_STRING,title='Project name'),
                'user': openapi.Schema(type=openapi.TYPE_STRING,title='Username'),
                'start_time': openapi.Schema(type=openapi.TYPE_STRING,title='Start time'),
                'end_time': openapi.Schema(type=openapi.TYPE_STRING,title='End time'),
                'duration': openapi.Schema(type=openapi.TYPE_NUMBER,title='Duration in seconds'),
                'description': openapi.Schema(type=openapi.TYPE_STRING,title='Description'),
            },
            required=['id', 'project', 'user', 'start_time', 'end_time', 'duration', 'description']
        )
    )

def get_update_project_schema():
    return openapi.Schema(
        "Update Project",
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING,title='Token'),
            'project': openapi.Schema(type=openapi.TYPE_STRING,title='Project name'),
            'name': openapi.Schema(type=openapi.TYPE_STRING,title='New project name'),
            'category': openapi.Schema(type=openapi.TYPE_STRING,title='Category'),
            'start_time': openapi.Schema(type=openapi.TYPE_STRING,title='Start Time'),
            'end_time': openapi.Schema(type=openapi.TYPE_STRING,title='End time'),
            'description': openapi.Schema(type=openapi.TYPE_STRING,title='Description'),
            'budget': openapi.Schema(type=openapi.TYPE_NUMBER,title='Budget'),
            'avatar_path': openapi.Schema(type=openapi.TYPE_STRING,title='Avatar path'),
        },
        required=['token', 'project']
    )

def get_datail_project_schema():
    return openapi.Schema(
        "Detail Project",
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING,title='Project name'),
            'category': openapi.Schema(type=openapi.TYPE_STRING,title='Category'),
            'start_time': openapi.Schema(type=openapi.TYPE_STRING,title='Start Time',pattern="YY-MM-DD hh:mm:ss"),
            'end_time': openapi.Schema(type=openapi.TYPE_STRING,title='End time',pattern="YY-MM-DD hh:mm:ss"),
            'description': openapi.Schema(type=openapi.TYPE_STRING,title='Description'),
            'budget': openapi.Schema(type=openapi.TYPE_NUMBER,title='Budget'),
            'avatar': openapi.Schema(type=openapi.TYPE_STRING,title='Avatar path'),
        },
        required=['name', 'category', 'start_time', 'end_time', 'description', 'budget', 'avatar']
    )


class SwaggerErrorSchema():

    def __init__(self):
        
        #field and non-filed errors for 'register' api
        self.register_non_field_errors = ['database error']
        self.register_field_errors = {
            "username": [
                "This field must be unique."
            ],
            "email": [
                "This field must be unique."
            ],
            "password": [
                "Ensure this field has at least 8 characters."
            ]
        }
        #field and non-filed errors for 'active-user' api
        self.active_user_non_filed_errors = ["token is not valid","username in not valid","you have not access"]
        self.active_user_field_errors = {
            "token": [
                "This field is required."
            ],
            "username": [
                "This field is required."
            ],
            "action": [
                "This field is required."
            ],
        }
        #field and non-filed errors for 'login' api
        self.login_non_field_errors = ["username/password is not valid","user is not active"]
        self.login_field_errors = {
            "username": [
                "This field is required."
            ],
            "password": [
                "This field is required."
            ],
        }
        #field and non-filed errors for 'delete-user' api
        self.delete_user_non_field_errors = ["token is not valid","you have not access","username in not valid"]
        self.delete_user_field_errors = {
            "token": [
                "This field is required."
            ],
            "username": [
                "This field is required."
            ],
        }
        #field and non-filed errors for 'update-user' api
        self.update_user_non_field_errors = ["token is not valid","username in not valid","you have not access",]
        self.update_user_field_errors = {
            "token": [
                "This field is required."
            ],
            "username": [
                "This field is required."
            ],
            "email": [
                "This field must be unique.",
            ],
            "password": [
                "Ensure this field has at least 8 characters."
            ],
        }
        #field and non-filed errors for 'list-users' api
        self.list_user_non_field_errors = ["token is not valid","you have not access",]
        self.list_user_field_errors = {
            "token": [
                "This field is required."
            ],
            "is_working": [
                "Must be a valid boolean."
            ],
        }
        #field and non-filed errors for 'detail-user' api
        self.detail_user_non_field_errors = ["token is not valid","you have not access",]
        self.detail_user_field_errors = {
            "token": [
                "This field is required."
            ],
            "username": [
                "This field is required."
            ],
        }
        #field and non-filed errors for 'time/manual' api
        self.time_manual_non_field_errors = ["token is not valid","project is not exist","user is not a member of the project"]
        self.time_manual_field_errors = {
            "token": [
                "This field is required."
            ],
            "project": [
                "This field is required."
            ],
            "start_time": [
                "This field is required."
            ],
            "end_time": [
                "This field is required."
            ],
            "description": [
                "This field is required."
            ],
        }
        #field and non-filed errors for 'time/auto' api
        self.time_auto_non_field_errors = [
            "token is not valid",
            "project is not exist",
            "user is not a member of the project",
            "you have an imcomplete time: 2020-12-30 20:30:45"]

        self.time_auto_field_errors = {
            "token": [
                "This field is required."
            ],
            "project": [
                "This field is required."
            ],
        }

        #field and non-filed errors for 'create-project' api
        self.create_project_non_field_errors = [
            "token is not valid",
            "You have not access"]

        self.create_project_field_errors = {
            "token": [
                "This field is required."
            ],
            "category": [
                "This field is required."
            ],
            "name": [
                "This field must be unique.",
            ],
            "avatar": [
                "Upload a valid image. The file you uploaded was either not an image or a corrupted image",
            ]
        }
        #field and non-filed errors for 'time/auto/stop' api
        self.time_auto_stop_non_field_errors = [
            "token is not valid",
            "there is no incomplete time for this user"]

        self.time_auto_stop_field_errors = {
            "token": [
                "This field is required."
            ],
            "description": [
                "This field is required."
            ],
            
        }
        #field and non-filed errors for 'add-to-project' api
        self.add_to_project_non_field_errors = [
            "token is not valid",
            "You have not access",
            "user is not exist",
            "project is not exist",
            "user already added to this project"]

        self.add_to_project_field_errors = {
            "token": [
                "This field is required."
            ],
            "description": [
                "This field is required."
            ],
        }
        #field and non-filed errors for 'list-projects' api
        self.list_project_non_field_errors = [
            "token is not valid",
            "You have not access"
            ]

        self.list_project_field_errors = {
            "token": [
                "This field is required."
            ],
            
        }
        #field and non-filed errors for 'list-times' api
        self.list_time_non_field_errors = [
            "token is not valid",
            "You have not access",
            "user is not exist",
            "must include at least one filter"
            ]

        self.list_time_field_errors = {
            "token": [
                "This field is required."
            ],
            
        }
        #field and non-filed errors for 'delete-time' api
        self.delete_time_non_field_errors = [
            "token is not valid",
            "time_id is not valid",
            "you have not access"
            ]

        self.delete_time_field_errors = {
            "token": [
                "This field is required."
            ],
            "time_id": [
                "This field is required."
            ],
            
        }
        #field and non-filed errors for 'update-time' api
        self.update_time_non_field_errors = [
            "token is not valid",
            "time_id is not valid",
            "you have not access",
            "project is not exist",
            "you are not member of project"
            ]

        self.update_time_field_errors = {
            "token": [
                "This field is required."
            ],
            "time_id": [
                "This field is required."
            ],
            
        }
        #field and non-filed errors for 'delete-project' api
        self.delete_project_non_field_errors = [
            "token is not valid",
            "you have not access",
            "project is not exist",
            ]

        self.delete_project_field_errors = {
            "token": [
                "This field is required."
            ],
            "project": [
                "This field is required."
            ],  
        }
        #field and non-filed errors for 'update-project' api
        self.update_project_non_field_errors = [
            "token is not valid",
            "you have not access",
            "project is not exist",
            ]
        self.update_project_field_errors = {
            "token": [
                "This field is required."
            ],
            "project": [
                "This field is required."
            ],  
            "name": [
                "This field must be unique."
            ],  
        }
        #field and non-filed errors for 'detail-project' api
        self.detail_project_non_field_errors = [
            "token is not valid",
            "you have not access",
            "project is not exist",
            ]

        self.detail_project_field_errors = {
            "token": [
                "This field is required."
            ],
            "project": [
                "This field is required."
            ],   
        }
        
        
    def schema_generator(self,non_field_error_list:list,field_error_dict:dict):

        schema = openapi.Schema(
                description="one or more of these errors may occur",
                title='Validation Error',
                type=openapi.TYPE_OBJECT,
                properties={
                    api_settings.NON_FIELD_ERRORS_KEY: openapi.Schema(
                        description='\n or \n'.join(non_field_error_list),
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(title='List of validation errors not related to any field',type=openapi.TYPE_STRING, example=non_field_error_list[0]),
                    ),
                },
            )
        field_schemas = {}
        for key in field_error_dict:
            field_schemas[key] = openapi.Schema(
                    description=field_error_dict[key][0],
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING,example=field_error_dict[key][0])
                )
        schema.properties = {**schema.properties,**field_schemas}
        return schema

    def get_schema(self,schema_name:str):

        """get custom schema for each API
        params:
        schema_name: (str) API url 
        schema_name options: 'register','active-user','login','delete-user','update-user','list-users','detail-user','time-manual','time-auto',
                                'time-auto-stop','create-project', 'list-projects', 'list-times','delete-time','update-time','delete-project',
                                'update-project', 'detail-project'
        """

        if schema_name=='register':
            return self.schema_generator(self.register_non_field_errors,self.register_field_errors)
        elif schema_name=='active-user':
            return self.schema_generator(self.active_user_non_filed_errors,self.active_user_field_errors)
        elif schema_name=='login':
            return self.schema_generator(self.login_non_field_errors,self.login_field_errors)
        elif schema_name=='delete-user':
            return self.schema_generator(self.delete_user_non_field_errors,self.delete_user_field_errors)
        
        elif schema_name=='update-user':
            return self.schema_generator(self.update_user_non_field_errors,self.update_user_field_errors)
        
        elif schema_name=='list-users':
            return self.schema_generator(self.list_user_non_field_errors,self.list_user_field_errors)
        
        elif schema_name=='detail-users':
            return self.schema_generator(self.detail_user_non_field_errors,self.detail_user_field_errors)
        
        elif schema_name=='time-manual':
            return self.schema_generator(self.time_manual_non_field_errors,self.time_manual_field_errors)
        
        elif schema_name=='time-auto':
            return self.schema_generator(self.time_auto_non_field_errors,self.time_auto_field_errors)
        
        elif schema_name=='time-auto-stop':
            return self.schema_generator(self.time_auto_stop_non_field_errors,self.time_auto_stop_field_errors)
        
        elif schema_name=='create-project':
            return self.schema_generator(self.create_project_non_field_errors,self.create_project_field_errors)
        
        elif schema_name=='add-to-project':
            return self.schema_generator(self.add_to_project_non_field_errors,self.add_to_project_field_errors)
        
        elif schema_name=='list-projects':
            return self.schema_generator(self.list_project_non_field_errors,self.list_project_field_errors)
        
        elif schema_name=='list-times':
            return self.schema_generator(self.list_time_non_field_errors,self.list_time_field_errors)
        
        elif schema_name=='delete-time':
            return self.schema_generator(self.delete_time_non_field_errors,self.delete_time_field_errors)
        
        elif schema_name=='update-time':
            return self.schema_generator(self.update_time_non_field_errors,self.update_time_field_errors)
        
        elif schema_name=='delete-project':
            return self.schema_generator(self.delete_project_non_field_errors,self.delete_project_field_errors)
        
        elif schema_name=='update-project':
            return self.schema_generator(self.update_project_non_field_errors,self.update_project_field_errors)
        
        elif schema_name=='detail-project':
            return self.schema_generator(self.detail_project_non_field_errors,self.detail_project_field_errors)
        else:
            pass
        
        
        
