from django.contrib import admin
from .models import *


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'taskid', 'add_time', 'limit_time']


admin.site.register(Task, TaskAdmin)


class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['task', 'mark']


admin.site.register(Evaluation, EvaluationAdmin)
