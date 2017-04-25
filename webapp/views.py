from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic.edit import (
    DeleteView,
    UpdateView,
    CreateView,
)
from django.views.generic import ListView
from django.forms import ModelForm
from webapp.models import Group, Student

from django.contrib.auth.mixins import LoginRequiredMixin


# ==> ListView doesn't provide post method
#
class HomeView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['form'] = GroupForm(prefix='group')
        return context


class GroupForm(ModelForm):

    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Group name'
        }
        self.fields['head'].widget.attrs = {
            'class': 'form-control',
        }
        # Student list are limited to childs
        self.fields['head'].queryset = Student.objects.filter(group=self.instance)
        #self.fields['head'].queryset = group.student_set.all()
        #print(kwargs)
        # print(self.fields['head'].queryset)


class StudentForm(ModelForm):

    class Meta:
        model = Student
        fields = '__all__'

    # http://stackoverflow.com/questions/401025/define-css-class-in-django-forms
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Student name'
        }
        self.fields['group'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['brd_date'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Date of birth',
        }
        self.fields['ticket'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Ticket number'
        }


class UpdateGroup(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "group.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateGroup, self).get_context_data(**kwargs)
        context['form_st'] = StudentForm(prefix='student')
        context['students'] = Student.objects.all().filter(group=self.kwargs['pk'])
        context.update(self.kwargs)
        print(context)
        return context

    def get_success_url(self):
        return reverse('update_group', kwargs={'pk': self.kwargs['pk']})


class UpdateStudent(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm

    template_name = "update_student.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateStudent, self).get_context_data(**kwargs)
        context['students'] = Student.objects.all().filter(group=Student.objects.get(pk=self.kwargs['pk']).group)
        context.update(self.kwargs)

        return context


class CreateGroup(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm

    def post(self, request, *args, **kwargs):
        if request.POST['group-name']:
            group_name = request.POST.get('group-name', False)
            # http://stackoverflow.com/questions/8133505/django-templateview-and-form
            Group.objects.create(name=group_name)
            return redirect('/')
        elif not request.POST['group-name']:
            return HttpResponse("Please enter the group")


class CreateStudent(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm

    def post(self, request, *args, **kwargs):

        if request.POST['student-name']:
            student_name = request.POST['student-name']
            student_brd_date = request.POST['student-brd_date']
            student_ticket = request.POST['student-ticket']

            Student.objects.create(
                name=student_name,
                brd_date=student_brd_date,
                ticket=student_ticket,
                group=Group.objects.get(pk=kwargs['pk'])
            )
            return redirect(
                # reverse('update_group', kwargs={'`k': kwargs['gr_pk']})
                reverse('update_group', kwargs={'pk': kwargs['pk']})
            )


class DeleteGroupView(LoginRequiredMixin, DeleteView):
    model = Group
    success_url = "/"


class DeleteStudentView(LoginRequiredMixin, DeleteView):
    model = Student

    def get_success_url(self):
        return reverse('update_group', kwargs={'pk': self.get_object().group.id})



"""
# ==> form_class and template_name are extra since
# ==> we need only post method
# ==> How are objects are getting saved?
class CreateGroup(FormView):
    model = Group
    form_class = GroupForm
    template_name = 'home.html'

    success_url = '/'

    def post(self, request, *args, **kwargs):
        print(request.POST)
        self.object = None
        return super(CreateGroup, self).post(request, *args, **kwargs)
"""



# ===> get classes shorterer
# ===> move all base classes to UpdateClasses and leave CreateClasses as it is
# ===> figure out how the validation, save or update methods work on Create/UpdateViews



# https://docs.djangoproject.com/en/1.10/topics/class-based-views/mixins/
# https://docs.djangoproject.com/en/1.10/ref/class-based-views/mixins/
# http://stackoverflow.com/questions/17192737/django-class-based-view-for-both-create-and-update
# http://stackoverflow.com/questions/19341568/listview-and-createview-in-one-template-django
# http://stackoverflow.com/questions/16931901/django-combine-detailview-and-formview
