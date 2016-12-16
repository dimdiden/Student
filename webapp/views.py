from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import  TemplateView, FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login
from webapp.models import Group, Student

class HomeTemplateView(TemplateView):

	template_name = "home.html"

	def get_context_data(self, **kwargs):
	    context = super(HomeTemplateView, self).get_context_data(**kwargs)
	    dic = {}
#populate dictionary dic with grups and number of the students
	    for obj in Group.objects.all():
			
	    	stdcount = Student.objects.filter(group = obj.id).count()
	    	dic.update({obj : stdcount})   	

	    context['groups'] = dic
	    return context



def newgroup(request):
	if request.method == "POST":
		group_name = request.POST.get("AddGroup")
		group = Group(name = group_name)
		group.save()
		return redirect('/')
		
	else:
		return redirect('/')

#def contact(request):
#	return render(request, 'basic.html', {'keys':['I\'m a programma', 'ded@email.com']})






