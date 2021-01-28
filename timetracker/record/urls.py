from record import views
from django.urls import path,re_path, include

urlpatterns= [
    re_path(r'^time/manual/$',views.TimeRecoringManualView.as_view(), name='time recording manual'),
    re_path(r'^time/auto/$',views.TimeRecoringAutoView.as_view(), name='time recording auto'),
    re_path(r'^time/auto/stop/$',views.TimeRecoringStopView.as_view(), name='stop auto time recording'),
    re_path(r'^create-project/$',views.ProjectCreateView.as_view(), name='create project'),
    re_path(r'^add-to-project/$',views.AddUserToProjectView.as_view(), name='add user to project'),
    re_path(r'^list-projects/$',views.ListProjectView.as_view(), name='list of projects'),
    re_path(r'^list-times/$',views.ListTimesView.as_view(), name='list of times'),
    re_path(r'^delete-time/$',views.TimeDeleteView.as_view(), name='delete time'),
    re_path(r'^update-time/$',views.TimeUpdateView.as_view(), name='update time'),
    re_path(r'^delete-project/$',views.ProjectDeleteView.as_view(), name='delete project'),
    re_path(r'^update-project/$',views.ProjectUpdateView.as_view(), name='update project'),
    re_path(r'^detail-project/$',views.ProjectDetailView.as_view(), name='detail of project'),
    re_path(r'^issues/$',views.ListIssueView.as_view(), name='list of issues'),

    
]