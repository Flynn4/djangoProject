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
    students = models.ManyToManyField(User, blank=True, related_name='students')
    mentor = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    isFinish = models.BooleanField(default=False)

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
    rater = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    peerReviewMark = models.IntegerField(default=0)
    mentorReviewMark = models.IntegerField(default=0)
    academicReviewMark = models.IntegerField(default=0)
    totalMark = models.IntegerField(default=0)
    averageMark = models.FloatField(default=0)
    peer_review_mark = models.ManyToManyField(Criterion, blank=True, through='PeerReviewMark',
                                              related_name='peer_review_mark')
    mentor_mark = models.ManyToManyField(Criterion, blank=True, through='MentorMark', related_name='mentor_mark')
    academic_mark = models.ManyToManyField(Criterion, blank=True, through='AcademicMark', related_name='academic_mark')

    def __str__(self):
        return self.task.name


class PeerReviewMark(models.Model):
    evaluation = models.ForeignKey(Evaluation, null=True, blank=True, default=None, on_delete=models.CASCADE)
    criterion = models.ForeignKey(Criterion, null=True, blank=True, default=None, on_delete=models.CASCADE)
    rater = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    mark = models.IntegerField(default=0)

    class Meta:
        db_table = 'peer_review_mark'


class MentorMark(models.Model):
    evaluation = models.ForeignKey(Evaluation, null=True, blank=True, default=None, on_delete=models.CASCADE)
    criterion = models.ForeignKey(Criterion, null=True, blank=True, default=None, on_delete=models.CASCADE)
    rater = models.ForeignKey(User, editable=False, null=True, blank=True, default=None, on_delete=models.CASCADE)
    mark = models.IntegerField(default=0)

    class Meta:
        db_table = 'mentor_mark'


class AcademicMark(models.Model):
    evaluation = models.ForeignKey(Evaluation, null=True, blank=True, default=None, on_delete=models.CASCADE)
    criterion = models.ForeignKey(Criterion, null=True, blank=True, default=None, on_delete=models.CASCADE)
    rater = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    mark = models.IntegerField(default=0)

    class Meta:
        db_table = 'academic_mark'


class Team(models.Model):
    teamId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    mentor = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE,
                               related_name='mentor')
    member = models.ManyToManyField(User, blank=True, related_name='member')

    def team_member(self):
        return ','.join([i.username for i in self.member.all()])


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, null=True, blank=True, default=None, on_delete=models.CASCADE)
    isStudent = models.BooleanField(default=True)
    isMentor = models.BooleanField(default=False)
    isStaff = models.BooleanField(default=False)
    team = models.ForeignKey(Team, null=True, blank=True, default=None, on_delete=models.CASCADE)


class TaskComment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, null=True, blank=True, default=None, on_delete=models.CASCADE)
    comment = models.TextField(default="")
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + '---' + self.task.name


class MentorComment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, null=True, blank=True, default=None, on_delete=models.CASCADE)
    comment = models.TextField(default="")
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + '---' + self.evaluation


class AcademicComment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, null=True, blank=True, default=None, on_delete=models.CASCADE)
    comment = models.TextField(default="")
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + '---' + self.evaluation
