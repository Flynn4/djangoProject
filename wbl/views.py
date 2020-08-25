import json
import time

from django.shortcuts import render, HttpResponse
from .models import *


def index(request):
    # Add all details into dict
    dict = {}
    return render(request, 'wbl/index.html', dict)


def profile(request):
    user = request.user
    role = UserProfile.objects.get(user=user).role
    print(role)
    criterions = role.role_have.all()
    print(criterions)
    return render(request, 'wbl/profile.html', {'criterions': criterions})


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
    criterions = request.POST.getlist('criterion_checkbox')
    print(criterions)
    if Task.objects.filter(name=name).count() == 1:
        return HttpResponse('Error')
    else:
        t = Task.objects.get_or_create(name=name, detail=detail, limit_time=limit_time)[0]
        for c in criterions:
            t.include_criterion.add(c)
        time.sleep(1)
        id = Task.objects.filter(name=name).values('taskId')[0]['taskId']
        return HttpResponse(id)


def task_edit(request, id):
    dict = {}
    if Task.objects.filter(taskId=id).count() > 0:
        dict['task'] = Task.objects.filter(taskId=id)[0]
        return render(request, 'wbl/task-edit.html', dict)
    else:
        return render(request, 'wbl/404.html')


def task_detail(request, id):
    dict = {}
    id = id.replace('/', '')
    dict['task'] = Task.objects.filter(taskId=id)[0]

    return render(request, 'wbl/task-detail.html', dict)


def evaluation_list(request):
    dict = {}
    dict['tasks'] = Task.objects.all()
    return render(request, 'wbl/evaulation-list.html', dict)


def evaluations(request, id):
    user = request.user
    e = Evaluation.objects.get_or_create(task_id=id, rater=user)[0]
    e.save()
    task = Task.objects.filter(taskId=id)[0]
    return render(request, 'wbl/evaluations.html', {'task': task, 'evaluation': e})


def peer_review(request, id):
    task = Task.objects.filter(taskId=id)[0]
    evaluations = Evaluation.objects.filter(task=task)
    return render(request, 'wbl/peer-review.html', {'task': task, 'evaluations': evaluations})


def evaluation_mentor(request, id):
    task = Task.objects.filter(taskId=id)[0]
    return render(request, 'wbl/evaluation-mentor.html', {'task': task})


def academic_evaluation(request, id):
    dict = {}
    dict['task'] = Task.objects.filter(taskId=id)[0]
    return render(request, 'wbl/academic-evaluation.html', dict)


def peer_review_detail(request, taskId, raterId):
    raterId = raterId.replace('/', '')
    task = Task.objects.filter(taskId=taskId)[0]
    rater = User.objects.filter(id=raterId)[0]
    evaluation = Evaluation.objects.filter(task=task, rater=rater)[0]
    for criterion in task.include_criterion.all():
        prm = PeerReviewMark.objects.get_or_create(evaluation=evaluation, rater=rater, criterion=criterion)
    marks = PeerReviewMark.objects.filter(evaluation=evaluation, rater=rater)
    return render(request, 'wbl/peer-review-detail.html', {'task': task, 'rater': rater, 'marks': marks, 'evaluation': evaluation})


def example_form(request):
    return render(request, 'wbl/example-form.html')


def choose_role(request):
    roles = Role.objects.all()
    return render(request, 'wbl/choose_role.html', {'roles': roles})


def get_choose_role(request):
    user = request.user
    print(user)
    role_name = request.POST.get('role')
    print(role_name)
    role = Role.objects.filter(name=role_name)[0]
    print(role)
    u = UserProfile.objects.get_or_create(user=user)[0]
    print(u)
    u.role = role
    u.save()
    if u.role.name == role_name:
        return HttpResponse('OK')
    else:
        return HttpResponse('Error')


def save_mark(request):
    user = request.user
    taskId = request.POST.get('taskId')
    totalMark = request.POST.get('totalMark')
    averageMark = request.POST.get('averageMark')
    criterionMark = json.loads(request.POST.getlist('criterionMark')[0])
    e = Evaluation.objects.get(task_id=taskId, rater=user)
    e.totalMark = totalMark
    e.averageMark = averageMark
    e.rater = user
    e.save()

    for c in criterionMark:
        criterion = Criterion.objects.get(name=c['name'])
        cm = PeerReviewMark.objects.get_or_create(evaluation=e, criterion=criterion, rater=user)[0]
        cm.mark = c['mark']
        print(cm)
        cm.save()

    print(e)
    return HttpResponse('OK')
