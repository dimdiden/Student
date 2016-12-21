from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView
from django.forms import ModelForm
from webapp.models import Group, Student


class HomeTemplateView(TemplateView):

    template_name = "home.html"

    def post(self, request, *args, **kwargs):
        if request.POST['name']:
            group_name = request.POST['name']
            # http://stackoverflow.com/questions/8133505/django-templateview-and-form
            Group.objects.create(name=group_name)
            return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        self.form = GroupForm()

        dic = {}
        # populate dictionary dic with grups and number of the students
        for obj in Group.objects.all():
            stdcount = Student.objects.filter(group=obj.id).count()
            dic.update({obj: [obj.name, stdcount, obj.head]})

        context['form'] = self.form
        context['groups'] = dic
        return context


class StudentListView(DetailView):

    model = Group
    template_name = "group.html"

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        # a = self.kwargs['pk']
        # print(a)
        self.group = get_object_or_404(Group, id=self.kwargs['pk'])
        self.form = StudentForm()

        context['form'] = self.form
        context['students'] = Student.objects.filter(group=self.group)
        context['group'] = Group.objects.get(id=self.kwargs['pk'])
        print(context)
        return context


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
            'placeholder': 'Date of birth'
        }
        self.fields['ticket'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Ticket number'
        }


class StudentListViewForm(TemplateView):

    template_name = "group.html"

    def get_context_data(self, **kwargs):
        context = super(StudentListViewForm, self).get_context_data(**kwargs)
        student_data = Student.objects.get(id=self.kwargs['st_pk'])
        # print(student_data.name)

        self.form = StudentForm(initial={
            'group': student_data.group,
            'name': student_data.name,
            'brd_date': student_data.brd_date,
            'ticket': student_data.ticket
        })

        context['form'] = self.form
        # print(self.kwargs['st_pk'])
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


"""
def newgroup(request):
    if request.method == "POST" and request.POST['AddGroup']:
        group_name = request.POST['AddGroup']

        Group.objects.create(name=group_name)
        return redirect('/')
    else:
        return HttpResponse('You havn\'t submitted data')
"""
# def contact(request):
# return render(request, 'basic.html', 
# {'keys':['I\'m a programma', 'ded@email.com']})
