import time

from django.shortcuts import render, HttpResponse
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
    dict = {}
    dict['tasks'] = Task.objects.all()
    return render(request, 'wbl/tasks.html', dict)


def task_add(request):
    return render(request, 'wbl/task-add.html')


def add_task(request):
    name = request.POST.get('name')
    detail = request.POST.get('detail')
    limit_time = request.POST.get('limit_time')
    if Task.objects.filter(name=name).count() == 1:
        return HttpResponse('Error')
    else:
        Task.objects.create(name=name, detail=detail, limit_time=limit_time)
        time.sleep(1)
        id = Task.objects.filter(name=name).values('taskid')[0]['taskid']
        return HttpResponse(id)


def task_edit(request, id):
    dict = {}
    if Task.objects.filter(taskid=id).count() > 0:
        dict['task'] = Task.objects.filter(taskid=id)[0]
        return render(request, 'wbl/task-edit.html', dict)
    else:
        return render(request, 'wbl/404.html')


def task_detail(request, id):
    dict = {}
    id = id.replace('/', '')
    dict['task'] = Task.objects.filter(taskid=id)[0]

    return render(request, 'wbl/task-detail.html', dict)



def evaluation_list(request):
    dict = {}
    dict['tasks'] = Task.objects.all()
    return render(request, 'wbl/evaulation-list.html', dict)


def evaluations(request, id):
    dict = {}
    dict['task'] = Task.objects.filter(taskid=id)[0]
    return render(request, 'wbl/evaluations.html', dict)


def peer_review(request, id):
    return render(request, 'wbl/peer-review.html')


def evaluation_mentor(request, id):
    return render(request, 'wbl/evaluation-mentor.html')


def academic_evaluation(request, id):
    dict = {}
    dict['task'] = Task.objects.filter(taskid=id)[0]
    return render(request, 'wbl/academic-evaluation.html', dict)


def detailed_evaluation(request):
    return render(request, 'wbl/detailed-evaluation.html')