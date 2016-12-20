from django.conf.urls import url
from django.views.generic import ListView, DetailView
from webapp.models import Group, Student
from . import views
from  webapp.views import HomeTemplateView, StudentListView

urlpatterns = [
	url(r'^$', HomeTemplateView.as_view(), name='home'),
#	url(r'^(?P<pk>\d+)$', DetailView.as_view(model = Group, template_name = 'group.html')),
	url(r'^group/(?P<pk>\d+)$', StudentListView.as_view(), name='group'),
	url(r'^newgroup/', views.newgroup, name='newgroup'),
]
