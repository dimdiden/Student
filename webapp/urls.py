from django.conf.urls import url
from django.views.generic import ListView, DetailView
from webapp.models import Group, Student
from . import views
from  webapp.views import HomeTemplateView

urlpatterns = [
	#url(r'^$', ListView.as_view(queryset = Group.objects.all(), template_name="home.html")),
	url(r'^$', HomeTemplateView.as_view(), name='home'),
	url(r'^(?P<pk>\d+)$', DetailView.as_view(model = Group, template_name = 'group.html')),
	#url(r'^$', views.index, name='index'),
	url(r'^contact/', views.contact, name='contact'),
	url(r'^newgroup/', views.newgroup, name='newgroup'),
]
