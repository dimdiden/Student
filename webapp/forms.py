from django.forms import ModelForm
from webapp.models import Group, Student


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

        # article = Article.objects.get(pk=1)
        # form = ArticleForm(instance=article)

        self.fields['head'].queryset = Student.objects.filter(group=self.instance)
        # self.fields['head'].queryset = group.student_set.all()


class StudentForm(ModelForm):

    class Meta:
        model = Student
        fields = [
            'first_name',
            'last_name',
            'group',
            'brd_date',
            'ticket'
        ]

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'First name'
        }
        self.fields['last_name'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Last name'
        }
        self.fields['group'].required = False
        self.fields['group'].empty_label = None
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
