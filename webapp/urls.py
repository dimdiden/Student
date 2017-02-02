from django.conf.urls import url
from webapp.views import (
    HomeView, DeleteStudentView,
    DeleteGroupView, CreateGroup,
    CreateStudent, UpdateGroup, UpdateStudent
)

urlpatterns = [
    url(r'^$',
        HomeView.as_view(), name='home'),
    url(r'^create_gr/$',
        CreateGroup.as_view(), name='create_group'),
    url(r'^create_st/(?P<gr_pk>\d+)$',
        CreateStudent.as_view(), name='create_student'),
    url(r'^update_gr/(?P<gr_pk>\d+)$',
        UpdateGroup.as_view(), name='update_group'),
    url(r'^update_st/(?P<gr_pk>\d+)/(?P<pk>\d+)$',
        UpdateStudent.as_view(), name='update_student'),
    url(r'^delete_st/(?P<pk>\d+)$',
        DeleteStudentView.as_view(), name='delete_student'),
    url(r'^delete_gr/(?P<gr_pk>\d+)$',
        DeleteGroupView.as_view(), name='delete_group'),
]
