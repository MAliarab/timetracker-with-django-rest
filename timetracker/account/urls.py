from account import views
from django.urls import path,re_path, include
from rest_framework import routers
# router = routers.DefaultRouter()
# router.register(r'register',views.UserViewSet)
urlpatterns= [
    re_path(r'^register',views.UserRegisterView.as_view()),
    re_path(r'^login',views.UserLoginView.as_view()),
    re_path(r'^active-user',views.UserActiveView.as_view()),
    re_path(r'^delete-user',views.UserDeleteView.as_view()),
    re_path(r'^update-user',views.UserUpdateView.as_view()),
    re_path(r'^list-users',views.ListUsersView.as_view()),
    re_path(r'^user-detail',views.UserDetailView.as_view()),

]