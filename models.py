from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey,ManyToManyField


# Create your models here.

class Projects(models.Model):
    projectId = models.IntegerField()
    projectDescription = models.CharField(max_length=30)
    projectTitle = models.CharField(max_length=15)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class Issue(models.Model):
    ISSUE_TYPE_CHOICES = (
        ('BUG', 'BUG'),
        ('TASK', 'TASK'),
        ('STORY', 'STORY'),
        ('EPIC', 'EPIC')
    )

    ISSUE_STATUS_CHOICES = (
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('In Review', 'In Review'),
        ('Code Complete', 'Code Complete'),
        ('Done','Done')
    )
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    #currentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    issueId = models.CharField(max_length=10)
    issueType = models.CharField(max_length=15,choices=ISSUE_TYPE_CHOICES)
    issueTitle = models.CharField(max_length=15)
    issueDescription = models.CharField(max_length=30)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE,related_name='reporter')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='assignee')
    issueStatus = models.CharField(max_length=20,choices=ISSUE_STATUS_CHOICES)
    labels = models.CharField(max_length=10)
    watchers = models.ManyToManyField(User)
    estimatedTime = models.DurationField()
    loggedTime = models.DurationField()


class Comment(models.Model):
    issue = models.ForeignKey(Issue,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    commentCreated = models.DateTimeField(auto_now_add=True)
    commentUpdated = models.DateTimeField(auto_now=True)
    comments = models.CharField(max_length=100)

class Sprint(models.Model):
    ACTIVE_STATUS = (
        ('OPEN','OPEN'),
        ('PROGRESS','PROGRESS'),
        ('CLOSED','CLOSED')
    )
    project = models.ForeignKey(Projects,on_delete=models.CASCADE,null=True)
    issue = models.ForeignKey(Issue,on_delete=models.CASCADE,blank=True)
    sprintUser = models.ForeignKey(User, on_delete=models.CASCADE)
    sprintId = models.AutoField(primary_key=True)
    sprintName = models.CharField(max_length=20)
    sprintStartDate = models.DateField()
    sprintEndDate = models.DateField()
    status = models.CharField(max_length=15,choices=ACTIVE_STATUS)

class UserDesignation(models.Model):
    DESIGNATION = (
        ('ADMIN','ADMIN'),
        ('MANAGER','MANAGER'),
        ('EMP','EMP')
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    designation = models.CharField(max_length=20, choices=DESIGNATION, default="EMP")
