from django.urls import reverse

from django.views.generic.edit import (
    DeleteView,
    UpdateView,
    CreateView,
)

from django.views.generic import FormView

from webapp.forms import GroupForm, StudentForm
from webapp.models import Group, Student

from django.contrib.auth.mixins import LoginRequiredMixin


class CreateGroup(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = "home.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(CreateGroup, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context


class UpdateGroup(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "group.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateGroup, self).get_context_data(**kwargs)

        students = Student.objects.all().filter(group=self.kwargs['pk'])

        context['form_gr'] = context.pop('form')
        context['form_st'] = StudentForm()
        context['students'] = students
        context.update(self.kwargs)
        return context

    def get_success_url(self):
        return reverse('update_group', kwargs={'pk': self.kwargs['pk']})


class CreateStudent(LoginRequiredMixin, FormView):
    http_method_names = [u'post']
    form_class = StudentForm
    template_name = 'group.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.group = Group.objects.get(pk=self.kwargs['pk'])
        self.object.save()
        return super(CreateStudent, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateStudent, self).get_context_data(**kwargs)

        group = Group.objects.get(pk=self.kwargs['pk'])
        students = Student.objects.all().filter(group=self.kwargs['pk'])

        context['form_st'] = context.pop('form')
        context['form_gr'] = GroupForm(instance=group, initial={
            'name': group.name,
            'head': group.head,
        })
        context['students'] = students
        context['group'] = group

        context.update(self.kwargs)
        return context

    def get_success_url(self):
        return reverse('update_group', kwargs={'pk': self.kwargs['pk']})


class UpdateStudent(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm

    template_name = "update_student.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateStudent, self).get_context_data(**kwargs)
        context['students'] = Student.objects.all().filter(
            group=Student.objects.get(pk=self.kwargs['pk']).group
        )
        context.update(self.kwargs)
        return context


class DeleteGroupView(LoginRequiredMixin, DeleteView):
    model = Group
    success_url = "/"


class DeleteStudentView(LoginRequiredMixin, DeleteView):
    model = Student

    def get_success_url(self):
        return reverse('update_group', kwargs={
            'pk': self.get_object().group.id
        })
