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
    criterions = role.role_have.all()

    # for criterion in criterions:
    #     prm = PeerReviewMark.objects.filter()
    #     for task in user.task_set.all():
    #         print(task.taskId)

    return render(request, 'wbl/profile.html', {'criterions': criterions})


def dashboard(request):
    return render(request, 'wbl/dashboard.html')


def tasks(request):
    user = request.user
    tasks = Task.objects.filter(students__exact=user)
    return render(request, 'wbl/tasks.html', {'tasks': tasks})


def task_add(request):
    user = request.user
    team = Team.objects.get(mentor=user)
    members = team.member.all()
    print(members)
    return render(request, 'wbl/task-add.html', {'members': members})


def add_task(request):
    user = request.user
    name = request.POST.get('name')
    detail = request.POST.get('detail')
    limit_time = request.POST.get('limit_time')
    criterions = request.POST.getlist('criterion_checkbox')
    students = request.POST.getlist('students')
    print(students)
    print(criterions)
    if Task.objects.filter(name=name).count() == 1:
        return HttpResponse('Error')
    else:
        t = Task.objects.get_or_create(name=name, detail=detail, limit_time=limit_time, mentor=user)[0]
        for c in criterions:
            t.include_criterion.add(c)
        for s in students:
            student = User.objects.get(username=s)
            t.students.add(student)
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
    id = id.replace('/', '')
    task = Task.objects.get(taskId=id)
    comments = TaskComment.objects.filter(task=task)

    return render(request, 'wbl/task-detail.html', {'task': task, 'comments': comments})


def finish_task(request):
    taskId = request.POST.get('taskId')
    task = Task.objects.get(taskId=taskId)
    task.isFinish = True
    task.save()
    return HttpResponse('OK')


def add_comment(request):
    user = request.user
    taskId = request.POST.get('taskId')
    task = Task.objects.get(taskId=taskId)
    evaluation = Evaluation.objects.get(task=task)
    comment = request.POST.get('comment')
    commentType = request.POST.get('commentType')
    print(commentType)
    if commentType == 'Task':
        tc = TaskComment.objects.get_or_create(user=user, task=task, comment=comment)
    elif commentType == 'Mentor':
        mc = MentorComment.objects.get_or_create(user=user, evaluation=evaluation, comment=comment)
    elif commentType == 'Academic':
        ac = AcademicComment.objects.get_or_create(user=user, evaluation=evaluation, comment=comment)
    else: return HttpResponse('Error')
    return HttpResponse('OK')



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


def mentor_review_detail(request, taskId):
    task = Task.objects.filter(taskId=taskId)[0]
    rater = task.mentor
    evaluation = Evaluation.objects.filter(task=task, rater=rater)[0]
    for criterion in task.include_criterion.all():
        mm = MentorMark.objects.get_or_create(evaluation=evaluation, rater=rater, criterion=criterion)
    marks = MentorMark.objects.filter(evaluation=evaluation, rater=rater)
    comments = MentorComment.objects.filter(evaluation=evaluation)
    return render(request, 'wbl/mentor-review-detail.html',
                  {'task': task, 'rater': rater, 'marks': marks, 'evaluation': evaluation, 'comments':comments})


def academic_review_detail(request, taskId):
    task = Task.objects.filter(taskId=taskId)[0]
    rater = task.mentor
    evaluation = Evaluation.objects.filter(task=task, rater=rater)[0]
    for criterion in task.include_criterion.all():
        am = AcademicMark.objects.get_or_create(evaluation=evaluation, rater=rater, criterion=criterion)
    marks = AcademicMark.objects.filter(evaluation=evaluation, rater=rater)
    comments = AcademicComment.objects.filter(evaluation=evaluation)
    return render(request, 'wbl/academic-review-detail.html',
                  {'task': task, 'rater': rater, 'marks': marks, 'evaluation': evaluation, 'comments':comments})


def peer_review_detail(request, taskId, raterId):
    raterId = raterId.replace('/', '')
    task = Task.objects.filter(taskId=taskId)[0]
    rater = User.objects.filter(id=raterId)[0]
    evaluation = Evaluation.objects.filter(task=task, rater=rater)[0]
    for criterion in task.include_criterion.all():
        prm = PeerReviewMark.objects.get_or_create(evaluation=evaluation, rater=rater, criterion=criterion)
    marks = PeerReviewMark.objects.filter(evaluation=evaluation, rater=rater)
    return render(request, 'wbl/peer-review-detail.html',
                  {'task': task, 'rater': rater, 'marks': marks, 'evaluation': evaluation})


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
    averageMark = request.POST.get('averageMark')
    peerReviewMark = request.POST.get('peerReviewMark')
    mentorReviewMark = request.POST.get('mentorReviewMark')
    academicReviewMark = request.POST.get('academicReviewMark')
    criterionMark = json.loads(request.POST.getlist('criterionMark')[0])
    e = Evaluation.objects.get(task_id=taskId, rater=user)
    if peerReviewMark is not None:
        e.peerReviewMark = peerReviewMark
    elif mentorReviewMark is not None:
        e.mentorReviewMark = mentorReviewMark
    elif academicReviewMark is not None:
        e.academicReviewMark = academicReviewMark
    e.totalMark = int(e.peerReviewMark) + int(e.mentorReviewMark) + int(e.academicReviewMark)
    e.averageMark = round(e.totalMark / 3, 1)
    e.rater = user
    e.save()

    for c in criterionMark:
        criterion = Criterion.objects.get(name=c['name'])
        if peerReviewMark is not None:
            cm = PeerReviewMark.objects.get_or_create(evaluation=e, criterion=criterion, rater=user)[0]
        elif mentorReviewMark is not None:
            cm = MentorMark.objects.get_or_create(evaluation=e, criterion=criterion, rater=user)[0]
        elif academicReviewMark is not None:
            cm = AcademicMark.objects.get_or_create(evaluation=e, criterion=criterion, rater=user)[0]
        cm.mark = c['mark']
        print(cm)
        cm.save()

    print(e)
    return HttpResponse('OK')
