from django.db import models

class Group(models.Model):
	name = models.CharField(max_length=10, null=True)
	head = models.ForeignKey('Student', related_name='+', null=True)

	def __str__(self):
#		return u'%s' % (self.name)
		return self.name

	def GetGroupCount(self):
		return self.objects.count()

#	def GetGroup():
#		return Group.objects.get(id=1)

class Student(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	name = models.CharField(max_length=140, null=True)
	brd_date = models.DateField(null=True)
	ticket = models.IntegerField(null=True, unique=True)

	def __str__(self):
		return self.name

#	def __str__(self):
#		return u'%s %s %s %s' % (self.group, self.name, self.brd_date, self.ticket)

	def GetStundentCount(self):
		return self.objects.count()



