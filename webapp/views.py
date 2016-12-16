from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import  TemplateView, FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login
from webapp.models import Group, Student

#def index(request):
	#return render(request, 'home.html')

class HomeTemplateView(TemplateView):
#	queryset = Group.objects.all()
	template_name = "home.html"
	model = Group
#	model = Student

	def get_context_data(self, **kwargs):
	    context = super(HomeTemplateView, self).get_context_data(**kwargs)
#	    context["groups"] = Group.objects.all()
	    context = { "groups" : Group.objects.all(), "fuck" : "FEYYAA" }

	    for i in Group.objects.all():
	    	print(i.name)

#	    context["fuck"] = "HAHAHAHAHA"
#	    print(context)
	    return context



def newgroup(request):
	if request.method == "POST":
		group_name = request.POST.get("AddGroup")
		group = Group(name = group_name)
		group.save()
		return redirect('/')
		
	else:
		return redirect('/')

def contact(request):
	return render(request, 'basic.html', {'keys':['I\'m a programma', 'ded@gmail.com']})


#class LoginFormView(FormView):
	#template_name = 'login.html'
	#form_class = AuthenticationForm
	#success_url = reverse_lazy('home')

	#def form_valid(self, form):
		#login(self.request, form.get_user())
		#return HttpResponseRedirect(self.success_url)





