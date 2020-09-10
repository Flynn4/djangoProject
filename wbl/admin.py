from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'taskId', 'add_time', 'limit_time']


admin.site.register(Task, TaskAdmin)


class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['task', 'task_id', 'rater', 'totalMark']


admin.site.register(Evaluation, EvaluationAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = ['roleId', 'name', 'criterion']


admin.site.register(Role, RoleAdmin)


class CriterionAdmin(admin.ModelAdmin):
    list_display = ['criterionId', 'name', 'associate_role']


admin.site.register(Criterion, CriterionAdmin)


class PeerReviewMarkAdmin(admin.ModelAdmin):
    list_display = ['evaluation', 'rater', 'criterion', 'mark']


admin.site.register(PeerReviewMark, PeerReviewMarkAdmin)


class MentorMarkAdmin(admin.ModelAdmin):
    list_display = ['evaluation', 'rater', 'criterion', 'mark']


admin.site.register(MentorMark, MentorMarkAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ['teamId', 'name', 'team_member']


admin.site.register(Team, TeamAdmin)


class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'task', 'comment', 'comment_time']


admin.site.register(TaskComment, TaskCommentAdmin)


class MentorCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'evaluation', 'comment', 'comment_time']


admin.site.register(MentorComment, MentorCommentAdmin)


class AcademicCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'evaluation', 'comment', 'comment_time']


admin.site.register(AcademicComment, AcademicCommentAdmin)


class UserCriterionMarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'criterion', 'evaluation', 'mark']


admin.site.register(UserCriterionMark, UserCriterionMarkAdmin)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
