from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Criterion(models.Model):
    criterionId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    detail = models.TextField(default=" ")

    def __str__(self):
        return str(self.name)

    def associate_role(self):
        return ','.join([i.name for i in self.role_set.all()])


class Task(models.Model):
    taskId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    detail = models.TextField(default=" ")
    add_time = models.DateTimeField(auto_now_add=True)
    limit_time = models.DateTimeField()
    progress = models.IntegerField(default=0)
    include_criterion = models.ManyToManyField(Criterion, blank=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    roleId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    role_have = models.ManyToManyField(Criterion, blank=True)

    def __str__(self):
        return self.name

    def criterion(self):
        return ','.join([i.name for i in self.role_have.all()])


# class Have(models.Model):
#     criterion = models.ForeignKey(Criterion, null=True, blank=True, default=None, on_delete=models.CASCADE)
#     role = models.ForeignKey(Role, null=True, blank=True, default=None, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'role_criterion'


class Evaluation(models.Model):
    task = models.ForeignKey(Task, null=True, blank=True, default=None, on_delete=models.CASCADE)
    mark = models.IntegerField(default=0)
    comment = models.TextField(default=" ")

    def __str__(self):
        return self.task.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, default=None, on_delete=models.CASCADE)
