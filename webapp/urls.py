from django.conf.urls import url
from webapp.views import HomeTemplateView, StudentListView, StudentListViewForm, DeleteStudentView, DeleteGroupView, CreateGroup, CreateStudent, UpdateGroup, UpdateStudent


urlpatterns = [
    url(r'^$',
        HomeTemplateView.as_view(), name='home'),
    url(r'^(?P<pk>\d+)$',
        StudentListView.as_view(), name='group'),
    url(r'^(?P<pk>\d+)/(?P<st_pk>\d+)$',
        StudentListViewForm.as_view(), name='studentform'),
    url(r'^delete_st/(?P<pk>\d+)$',
        DeleteStudentView.as_view(), name='delete_student'),
    url(r'^delete_gr/(?P<pk>\d+)$',
        DeleteGroupView.as_view(), name='delete_group'),
    url(r'^create_gr/$',
        CreateGroup.as_view(), name='create_group'),
    url(r'^create_st/$',
        CreateStudent.as_view(), name='create_student'),
    url(r'^update_gr/(?P<pk>\d+)$',
        UpdateGroup.as_view(), name='update_group'),
    url(r'^update_st/(?P<pk>\d+)/(?P<st_pk>\d+)$',
        UpdateStudent.as_view(), name='update_student')
]
