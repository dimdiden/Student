from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.forms import ModelForm
from webapp.models import Group, Student


class HomeTemplateView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        self.form = GroupForm(prefix='group')

        dic = {}
        # populate dictionary dic with grups and number of the students
        for obj in Group.objects.all():
            stdcount = Student.objects.filter(group=obj.id).count()
            dic.update({obj: stdcount})

        context['form'] = self.form
        context['groups'] = dic
        return context


class StudentListView(DetailView):

    model = Group
    template_name = "group.html"

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)

        self.group = get_object_or_404(Group, id=self.kwargs['pk'])
        self.form_st = StudentForm(prefix='student')
        self.form_gr = GroupForm(
            initial={
                'name': self.group.name,
                'head': self.group.head
            },
            prefix='group'
        )

        context['form_st'] = self.form_st
        context['form_gr'] = self.form_gr
        context['students'] = Student.objects.filter(group=self.group)
        context['group'] = self.group
        # print(context)
        return context


class StudentListViewForm(TemplateView):

    template_name = "update_student.html"

    def get_context_data(self, **kwargs):
        context = super(StudentListViewForm, self).get_context_data(**kwargs)
        self.group = get_object_or_404(Group, id=self.kwargs['pk'])
        student = Student.objects.get(id=self.kwargs['st_pk'])
        # print(student_data.name)

        self.form = StudentForm(
            initial={
                'group': student.group,
                'name': student.name,
                'brd_date': student.brd_date,
                'ticket': student.ticket
            },
            prefix='student'
        )
        context['for_del'] = student
        context['form_st'] = self.form
        context['students'] = Student.objects.filter(group=self.group)
        context['group'] = self.group
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


class CreateStudent(CreateView):
    model = Student
    form_class = StudentForm

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        if request.POST['student-name']:
            student_group = request.POST['student-group']
            student_name = request.POST['student-name']
            student_brd_date = request.POST['student-brd_date']
            student_ticket = request.POST['student-ticket']

            # print(request.POST)
            Student.objects.create(
                name=student_name,
                brd_date=student_brd_date,
                ticket=student_ticket,
                group=Group.objects.get(id=student_group)
            )
            # a = reverse('group', kwargs={'pk': student_group})
            # print(a)
            return redirect(reverse('group', kwargs={'pk': student_group}))


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


class DeleteStudentView(DeleteView):
    model = Student

    def get_success_url(self):
        item = self.get_object()
        self.item = item.group.id
        # print(self.item)           # -> 404
        return reverse('group', kwargs={'pk': self.item})


class DeleteGroupView(DeleteView):
    model = Group
    success_url = "/"
