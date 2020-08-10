from django.shortcuts import render
from .models import *


def index(request):
    # Add all details into dict
    dict = {}
    return render(request, 'wbl/index.html', dict)

def profile(request):
    return render(request, 'wbl/profile.html')


def dashboard(request):
    return render(request, 'wbl/dashboard.html')


def tasks(request):
    dict ={}
    dict['tasks'] = Task.objects.all()
    return render(request, 'wbl/tasks.html', dict)


def task_add(request):
    return render(request, 'wbl/task-add.html')


def task_edit(request):
    return render(request, 'wbl/task-edit.html')


def task_detail(request):
    return render(request, 'wbl/task-detail.html')


def peer_review(request):
    return render(request, 'wbl/peer-review.html')
