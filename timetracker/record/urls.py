from record import views
from django.urls import path,re_path, include

urlpatterns= [
    re_path(r'^time/manual',views.TimeRecoringManualView.as_view(), name='time recording manual'),
    re_path(r'^time/auto',views.TimeRecoringManualView.as_view(), name='time recording manual'),
    re_path(r'^create-project',views.ProjectCreateView.as_view(), name='create project'),
    re_path(r'^add-to-project',views.AddUserToProjectView.as_view(), name='add user to project'),



]