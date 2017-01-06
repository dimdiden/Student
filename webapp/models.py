from django.db import models
from django.core.urlresolvers import reverse

# ==> create is_head  field to the Student model
# ==> use group.student_set.all() to limit the selection

class Group(models.Model):
    name = models.CharField(max_length=10, null=True)
    head = models.OneToOneField(
        'Student',
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'group': 2},
    )
    # head = models.ForeignKey('Student', related_name='+', null=True, unique=True)

    def __str__(self):
        # return u'%s' % (self.name)
        return self.name

    def get_student_count(self):
        return Student.objects.filter(group=self.id).count()

    def get_absolute_url(self):
        return reverse('group', kwargs={'pk': str(self.id)})


class Student(models.Model):

    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    name = models.CharField(max_length=140, null=True)
    brd_date = models.DateField(null=True)
    ticket = models.IntegerField(null=True, unique=True)

    def __str__(self):
        return self.name

    def GetStundentCount(self):
        return self.objects.count()

    def get_absolute_url(self):
        print(self.group.id)
        return reverse('studentform', kwargs={
            'pk': self.group.id,
            'st_pk': self.id
        })
