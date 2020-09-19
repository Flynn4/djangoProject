import json
import time

from django.shortcuts import render, HttpResponse
from .models import *


def index(request):
    # Add all details into dict
    dict = {}
    return render(request, 'wbl/dashboard.html', dict)


def profile(request):
    user = request.user
    role = UserProfile.objects.get(user=user).role
    criterions = role.role_have.all()
    tasks = []
    for criterion in criterions:
        for task in criterion.task_set.all().filter(students__exact=user):
            totalPRM = 0
            for prm in PeerReviewMark.objects.filter(evaluation__task_id=task.taskId, criterion=criterion):
                totalPRM += prm.mark
            totalMM = 0
            for mm in MentorMark.objects.filter(evaluation__task_id=task.taskId, criterion=criterion):
                totalMM += mm.mark
            totalMark = totalPRM + totalMM
            tasks.append([criterion, task, totalPRM, totalMM, totalMark])

    return render(request, 'wbl/profile.html', {'criterions': criterions, 'tasks': tasks})


def dashboard(request):
    return render(request, 'wbl/dashboard.html')


def tasks(request):
    user = request.user
    if user.userprofile.isStudent:
        tasks = Task.objects.filter(students__exact=user)
    else:
        tasks = Task.objects.filter(mentor=user)
    return render(request, 'wbl/tasks.html', {'tasks': tasks})


def task_add(request):
    user = request.user
    if not Team.objects.filter(mentor=user).count() == 0:
        team = Team.objects.get(mentor=user)
        print(team)
        members = team.member.all()
        print(members)
        return render(request, 'wbl/task-add.html', {'members': members})
    return render(request, 'wbl/task-add.html', {'members': None})


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


def delete_task(request):
    user = request.user
    taskId = request.POST.get('taskId')
    print(user)
    print(taskId)
    if not user.userprofile.isStudent:
        Task.objects.filter(taskId=taskId).delete()
        return HttpResponse('OK')


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
    comment = request.POST.get('comment')
    commentType = request.POST.get('commentType')
    print(commentType)
    if commentType == 'Task':
        tc = TaskComment.objects.get_or_create(user=user, task=task, comment=comment)
    elif commentType == 'Mentor':
        evaluation = Evaluation.objects.get(task=task)
        mc = MentorComment.objects.get_or_create(user=user, evaluation=evaluation, comment=comment)
    elif commentType == 'Academic':
        evaluation = Evaluation.objects.get(task=task)
        ac = AcademicComment.objects.get_or_create(user=user, evaluation=evaluation, comment=comment)
    else:
        return HttpResponse('Error')
    return HttpResponse('OK')


def evaluation_list(request):
    user = request.user
    if user.userprofile.isStudent:
        tasks = Task.objects.filter(students__exact=user)
    elif user.userprofile.isMentor:
        tasks = Task.objects.filter(mentor=user)
    elif user.userprofile.isStaff:
        tasks = Task.objects.all()
    return render(request, 'wbl/evaulation-list.html', {'tasks': tasks})


def evaluations(request, id):
    user = request.user
    e = Evaluation.objects.get_or_create(task_id=id)[0]
    if user.userprofile.isMentor:
        e.rater = user
    e.save()
    task = Task.objects.filter(taskId=id)[0]
    return render(request, 'wbl/evaluations.html', {'task': task, 'evaluation': e})


def peer_review(request, id):
    task = Task.objects.filter(taskId=id)[0]
    evaluation = Evaluation.objects.get(task_id=id)
    reviews = []
    for student in task.students.all():
        total = 0
        for prm in PeerReviewMark.objects.filter(evaluation=evaluation, rater=student):
            total += prm.mark
        reviews.append((student, total))
    return render(request, 'wbl/peer-review.html', {'task': task, 'reviews': reviews})


def mentor_review_detail(request, taskId):
    task = Task.objects.filter(taskId=taskId)[0]
    rater = task.mentor
    evaluation = Evaluation.objects.filter(task=task)[0]
    for criterion in task.include_criterion.all():
        mm = MentorMark.objects.get_or_create(evaluation=evaluation, rater=rater, criterion=criterion)
    marks = MentorMark.objects.filter(evaluation=evaluation, rater=rater)
    comments = MentorComment.objects.filter(evaluation=evaluation)
    return render(request, 'wbl/mentor-review-detail.html',
                  {'task': task, 'rater': rater, 'marks': marks, 'evaluation': evaluation, 'comments': comments})


def academic_review_detail(request, taskId):
    task = Task.objects.filter(taskId=taskId)[0]
    rater = task.mentor
    evaluation = Evaluation.objects.filter(task=task)[0]
    comments = AcademicComment.objects.filter(evaluation=evaluation)
    return render(request, 'wbl/academic-review-detail.html',
                  {'task': task, 'rater': rater, 'evaluation': evaluation, 'comments': comments})


def peer_review_detail(request, taskId, raterId):
    raterId = raterId.replace('/', '')
    task = Task.objects.filter(taskId=taskId)[0]
    rater = User.objects.filter(id=raterId)[0]
    evaluation = Evaluation.objects.filter(task=task)[0]
    for criterion in task.include_criterion.all():
        prm = PeerReviewMark.objects.get_or_create(evaluation=evaluation, rater=rater, criterion=criterion)
    marks = PeerReviewMark.objects.filter(evaluation=evaluation, rater=rater)
    totalMark = 0
    for prm in PeerReviewMark.objects.filter(evaluation=evaluation, rater=rater):
        totalMark += prm.mark
    return render(request, 'wbl/peer-review-detail.html',
                  {'task': task, 'rater': rater, 'marks': marks, 'totalMark': totalMark})


def choose_role(request):
    roles = Role.objects.all()
    return render(request, 'wbl/choose_role.html', {'roles': roles})


def get_choose_role(request):
    user = request.user
    role_name = request.POST.get('role')
    role = Role.objects.filter(name=role_name)[0]
    u = UserProfile.objects.get_or_create(user=user)[0]
    if u.isMentor:
        name = 'Team ' + user.username
        t = Team.objects.get_or_create(name=name, mentor=user, role=role)[0]
        u.role = role
        u.save()
    elif u.isStudent:
        u.role = role
        u.save()
        for team in Team.objects.filter(role=role):
            if team.member.count() <= 4:
                team.member.add(user)
                team.save()
                break
    if u.role.name == role_name:
        return HttpResponse('OK')
    else:
        return HttpResponse('Error')


def save_mark(request):
    user = request.user
    taskId = request.POST.get('taskId')
    peerReviewMark = request.POST.get('peerReviewMark')
    mentorReviewMark = request.POST.get('mentorReviewMark')
    criterionMark = json.loads(request.POST.getlist('criterionMark')[0])
    e = Evaluation.objects.get(task_id=taskId)

    for c in criterionMark:
        criterion = Criterion.objects.get(name=c['name'])
        if peerReviewMark is not None:
            cm = PeerReviewMark.objects.get_or_create(evaluation=e, criterion=criterion, rater=user)[0]
        elif mentorReviewMark is not None:
            cm = MentorMark.objects.get_or_create(evaluation=e, criterion=criterion, rater=user)[0]
        cm.mark = c['mark']
        cm.save()

    if mentorReviewMark is not None:
        e.mentorReviewMark = mentorReviewMark
    elif peerReviewMark is not None:
        total = 0
        for prm in PeerReviewMark.objects.filter(evaluation=e):
            total += prm.mark
        e.peerReviewMark = total
    e.totalMark = int(e.peerReviewMark) + int(e.mentorReviewMark)
    e.averageMark = round(e.totalMark / 2, 1)
    e.rater = user
    e.save()

    return HttpResponse('OK')


def academic_pass(request):
    user = request.user
    taskId = request.POST.get('taskId')
    e = Evaluation.objects.get(task_id=taskId)
    e.isPass = True
    e.save()
    task = Task.objects.get(taskId=taskId)
    students = task.students.all()
    for student in students:
        for criterion in task.include_criterion.all():
            ucm = UserCriterionMark.objects.get_or_create(user=student, evaluation=e, criterion=criterion)[0]
            pm = 0
            for prm in PeerReviewMark.objects.filter(evaluation=e, criterion=criterion):
                pm += prm.mark
            mm = MentorMark.objects.get(evaluation=e, criterion=criterion).mark
            ucm.mark = pm + mm
            ucm.save()

    for student in students:
        graduate = True
        for criterion in student.userprofile.role.role_have.all():
            total = 0
            print(UserCriterionMark.objects.filter(user=student, criterion=criterion))
            for ucm in UserCriterionMark.objects.filter(user=student, criterion=criterion):
                total += ucm.mark
            print('Total Mark: ' + str(total))
            if total < 20:
                graduate = False
                break

        if graduate is True:
            student.userprofile.isGraduate = True
            print('Graduate success!')
            student.userprofile.save()

    return HttpResponse('OK')
