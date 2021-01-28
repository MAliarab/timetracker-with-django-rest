from django.db import models
from account.models import User
# Create your models here.
import jdatetime
import pytz
# jdatetime.datetime.now(pytz.timezone('Asia/Tehran'))

def nameFile(instance, filename):
    return '/'.join(['images', str(instance.name), filename])

class Project(models.Model):

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    start_time = models.DateTimeField(default=None)
    end_time = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True,default=None)
    avatar = models.ImageField(null=True, blank=True,default=None,upload_to='avatar/')
    budget = models.PositiveIntegerField(null=True, blank=True,default=None)
    def __str__(self):
        return str(self.id)+"_"+self.name

class Time(models.Model):

    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    issue_id = models.IntegerField(null=True, blank=True, default=None)
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + " - " + self.project.name + " - " + self.user.username + " - " + str(self.start_time)
    

class ProjectUser(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.project.name + " - " + self.user.username

