from django.conf.urls import url
from . import views
from webapp.views import HomeTemplateView, StudentListView, StudentListViewForm


urlpatterns = [
    url(r'^$', HomeTemplateView.as_view(), name='home'),
# url(r'^(?P<pk>\d+)$', DetailView.as_view(model = Group, template_name = 'group.html')),
    url(r'^newgroup/', views.newgroup, name='newgroup'),
    url(r'^group/(?P<pk>\d+)$', StudentListView.as_view(), name='group'),
    url(r'^group/(?P<pk>\d+)/(?P<st_pk>\d+)$', StudentListViewForm.as_view(), name='studentform')
]
