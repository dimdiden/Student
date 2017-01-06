from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, FormView
from django.views.generic.edit import DeleteView, UpdateView, CreateView, ModelFormMixin, ProcessFormView
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin
from django.forms import ModelForm
from webapp.models import Group, Student


# ==> ListView doesn't provide post method
#
class HomeView(ListView):

    model = Group
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['form'] = GroupForm(prefix='group')
        return context


class StudentListView(ListView):

    model = Student
    template_name = "group.html"

    def get_queryset(self):
        qs = super(StudentListView, self).get_queryset()
        return qs.filter(group=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        self.group = get_object_or_404(Group, id=self.kwargs['pk'])
        context['form_st'] = StudentForm(prefix='student')
        context['form_gr'] = GroupForm(
            initial={
                'name': self.group.name,
                'head': self.group.head
            },
            prefix='group',
        )
        context.update(self.kwargs)
        return context


class StudentListViewForm(ListView):

    model = Student
    template_name = "update_student.html"

    def get_queryset(self):
        qs = super(StudentListViewForm, self).get_queryset()
        return qs.filter(group=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(StudentListViewForm, self).get_context_data(**kwargs)
        self.group = get_object_or_404(Group, id=self.kwargs['pk'])
        self.student = get_object_or_404(Student, id=self.kwargs['st_pk'])

        context['form_st'] = StudentForm(
            initial={
                'group': self.student.group,
                'name': self.student.name,
                'brd_date': self.student.brd_date,
                'ticket': self.student.ticket
            },
            prefix='student'
        )
        context.update(self.kwargs)
        print(context)
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
        self.fields['head'].queryset = group.student_set.all()
        print(kwargs)
        #print(self.fields['head'].queryset)


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


class CreateGroup(CreateView):
    model = Group
    form_class = GroupForm

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.POST['group-name']:
            group_name = request.POST.get('group-name', False)
            # http://stackoverflow.com/questions/8133505/django-templateview-and-form
            Group.objects.create(name=group_name)
            return redirect('/')
        elif not request.POST['group-name']:
            return HttpResponse("Please enter the group")


"""
# ==> form_class and template_name are extra since
# ==> we need only post method
# ==> How are objects getting saved?
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


class CreateStudent(CreateView):
    model = Student
    form_class = StudentForm

    def post(self, request, *args, **kwargs):
        print(kwargs)
        if request.POST['student-name']:
            student_name = request.POST['student-name']
            student_brd_date = request.POST['student-brd_date']
            student_ticket = request.POST['student-ticket']

            Student.objects.create(
                name=student_name,
                brd_date=student_brd_date,
                ticket=student_ticket,
                group=Group.objects.get(id=kwargs['pk'])
            )
            return redirect(reverse('group', kwargs={'pk': kwargs['pk']}))


class UpdateGroup(UpdateView):
    model = Group
    form_class = GroupForm

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.POST['group-name'] and request.POST['group-head']:
            group_name = request.POST.get('group-name')
            request_head = request.POST.get('group-head', 0)
            print(request_head)
            group_head = Student.objects.get(id=request_head)

            # http://stackoverflow.com/questions/8133505/django-templateview-and-form
            Group.objects.select_for_update().filter(id=kwargs['pk']).update(
                name=group_name,
                head=group_head
            )
        elif not request.POST['group-head']:
            group_name = request.POST.get('group-name')
            Group.objects.select_for_update().filter(id=kwargs['pk']).update(
                name=group_name,
            )
        else:
            return HttpResponse("Something going wrong")
        return redirect(reverse('group', kwargs={'pk': self.kwargs['pk']}))


class UpdateStudent(UpdateView):
    model = Student
    form_class = StudentForm

    def post(self, request, *args, **kwargs):
        if request.POST['student-name']:
            student_group = request.POST['student-group']
            student_name = request.POST['student-name']
            student_brd_date = request.POST['student-brd_date']
            student_ticket = request.POST['student-ticket']

            print(request.POST)
            Student.objects.select_for_update().filter(id=kwargs['st_pk']).update(
                name=student_name,
                brd_date=student_brd_date,
                ticket=student_ticket,
                group=Group.objects.get(id=student_group)
            )
            # a = reverse('group', kwargs={'pk': student_group})
            # print(a)
            return redirect(reverse('group', kwargs={'pk': student_group}))


class DeleteGroupView(DeleteView):
    model = Group
    success_url = "/"


class DeleteStudentView(DeleteView):
    model = Student

    def get_success_url(self):
        item = self.get_object()
        return reverse('group', kwargs={'pk': item.group.id})

#===> get classes shorterer

# https://docs.djangoproject.com/en/1.10/topics/class-based-views/mixins/
# https://docs.djangoproject.com/en/1.10/ref/class-based-views/mixins/
# http://stackoverflow.com/questions/17192737/django-class-based-view-for-both-create-and-update
# http://stackoverflow.com/questions/19341568/listview-and-createview-in-one-template-django
# http://stackoverflow.com/questions/16931901/django-combine-detailview-and-formview
