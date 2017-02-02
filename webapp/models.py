from django.db import models
from django.core.urlresolvers import reverse


class Group(models.Model):
    name = models.CharField(max_length=10, null=True)
    head = models.OneToOneField(
        'Student',
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        # limit_choices_to={'group': 2},
    )

    def __str__(self):
        return self.name

    def get_student_count(self):
        return self.student_set.all().count()

    def get_absolute_url(self):
        return reverse('update_group', kwargs={'pk': str(self.id)})


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
        return reverse('update_student', kwargs={
            'gr_pk': self.group.id,
            'pk': self.id
        })
