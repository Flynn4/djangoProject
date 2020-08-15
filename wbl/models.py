from django.db import models


# Create your models here.
class Task(models.Model):
    taskid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    detail = models.TextField(default=" ")
    add_time = models.DateTimeField(auto_now_add=True)
    limit_time = models.DateTimeField()
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    # def tags(self):
    #     return ','.join([i.name for i in self.game_type.all()])


class Evaluation(models.Model):
    task = models.ForeignKey(Task, null=True, blank=True, default=None, on_delete=models.CASCADE)
    mark = models.IntegerField(default=0)
    comment = models.TextField(default=" ")

    def __str__(self):
        return self.task.name
